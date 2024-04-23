import pickle

import tensorflow as tf
import numpy as np
from keras.src.regularizers import regularizers
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model, load_model

import json

with open('data/intents.json', 'r') as f:
    data = json.load(f)


def clean(line):
    cleaned_line = ''
    for char in line:
        if char.isalpha():
            cleaned_line += char
        else:
            cleaned_line += ' '
    cleaned_line = ' '.join(cleaned_line.split())
    return cleaned_line


# list of intents
intents = []
unique_intents = []
# all text data to create a corpus
text_input = []
# dictionary mapping intent with appropriate response
response_for_intent = {}
for intent in data['intents']:
    # list of unique intents
    if intent['intent'] not in unique_intents:
        unique_intents.append(intent['intent'])
    for text in intent['text']:
        # cleaning is done before adding text to corpus
        text_input.append(clean(text))
        intents.append(intent['intent'])

tokenizer = Tokenizer(filters='', oov_token='<unk>')
tokenizer.fit_on_texts(text_input)
sequences = tokenizer.texts_to_sequences(text_input)
padded_sequences = pad_sequences(sequences, padding='pre')
print('Shape of Input Sequence:', padded_sequences.shape)
print(padded_sequences[:5])

intent_to_index = {}
categorical_target = []
index = 0

for intent in intents:
    if intent not in intent_to_index:
        intent_to_index[intent] = index
        index += 1
    categorical_target.append(intent_to_index[intent])

num_classes = len(intent_to_index)
print('Number of Intents :', num_classes)

# Convert intent_to_index to index_to_intent
index_to_intent = {index: intent for intent, index in intent_to_index.items()}
print(index_to_intent)

categorical_vec = tf.keras.utils.to_categorical(categorical_target,
                                                num_classes=num_classes)

print('Shape of Categorical', categorical_vec.shape)
print(categorical_vec[:5])

epochs = 15
embed_dim = 300
lstm_num = 50
output_dim = categorical_vec.shape[1]
input_dim = len(unique_intents)
print("Input Dimension :{},\nOutput Dimension :{}".format(input_dim, output_dim))

x, x_test, y, y_test = train_test_split(padded_sequences, categorical_vec)
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(len(tokenizer.word_index) + 1, embed_dim),
    tf.keras.layers.LSTM(lstm_num, dropout=0.1, kernel_regularizer=regularizers.L2(0.001)),
    tf.keras.layers.Dense(lstm_num, activation='relu', kernel_regularizer=regularizers.L2(0.001)),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(output_dim, activation='softmax')
])

#model.summary()

Nadam = tf.keras.optimizers.Nadam(learning_rate=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(loss='categorical_crossentropy', optimizer=Nadam, metrics=['accuracy'])

history = model.fit(x, y, epochs=epochs, batch_size=32, verbose=1,
                    validation_data=(x_test, y_test))

base_model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(len(tokenizer.word_index) + 1, embed_dim),
    tf.keras.layers.LSTM(lstm_num,),
    tf.keras.layers.Dense(output_dim, activation='softmax')
])

Nadam = tf.keras.optimizers.Nadam(learning_rate=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
base_model.compile(loss='categorical_crossentropy', optimizer=Nadam, metrics=['accuracy', 'loss'])

base_history = model.fit(x, y, epochs=epochs, batch_size=32, verbose=1,
                    validation_data=(x_test, y_test))

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for accuracy
plt.plot(base_history.history['accuracy'])
plt.plot(base_history.history['val_accuracy'])
plt.title('base model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(base_history.history['loss'])
plt.plot(base_history.history['val_loss'])
plt.title('base model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()



test_text_inputs = ["Indeed"]

test_intents = ["giving_answer"]

'''test_sequences = tokenizer.texts_to_sequences(test_text_inputs)
test_padded_sequences = pad_sequences(test_sequences,  padding='pre')
test_labels = np.array([unique_intents.index(intent) for intent in test_intents])
test_labels = tf.keras.utils.to_categorical(test_labels, num_classes=num_classes)
loss, accuracy = model.evaluate(test_padded_sequences, test_labels)'''

tokens = tokenizer.texts_to_sequences(test_text_inputs)
tokens = pad_sequences(tokens, maxlen=6000)
prediction = model.predict(np.array(tokens))
pred = np.argmax(prediction)
classes = ['oos', 'affirm_ready', 'affirm_hint', 'giving_answer', 'need_hint', 'affirm',
           "decline_ready", "decline_hint", 'decline', 'greetings']
print(prediction)
print(classes[pred])
model.save('models/Intent_Classification.keras')

with open('utils/tokenizer.pkl', 'wb') as file:
    pickle.dump(tokenizer, file)

model2 = load_model('models/Intent_Classification.keras')
model2.compile(loss='categorical_crossentropy', optimizer=Nadam, metrics=['accuracy'])

with open('utils/tokenizer.pkl', 'rb') as handle:
    tokenizer2 = pickle.load(handle)

tokens2 = tokenizer2.texts_to_sequences(test_text_inputs)
tokens2 = pad_sequences(tokens2, maxlen=6000)
prediction2 = model2.predict(np.array(tokens2))
pred2 = np.argmax(prediction2)
print(prediction2)
print(classes[pred2])
