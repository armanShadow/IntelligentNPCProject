import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


class StateTracker:
    def __init__(self, states, rl_states):
        self.states = states
        self.rlStates = rl_states

    def getStates(self):
        return self.states

    def getRLStates(self):
        return self.rlStates

    def updateStates(self, new_states):
        self.states.update(new_states)

    def updateRLStates(self, new_states):
        self.rlStates.update(new_states)


class DialogueManager:
    def __init__(self, model_path, tokenizer_path, states, rl_states):
        self.intentClassifier = self.__load_model(model_path)
        self.tokenizer = self.__load_tokenizer(tokenizer_path)
        self.state_tracker = StateTracker(states, rl_states)

    @staticmethod
    def __load_model(path):
        model = load_model(path)
        Nadam = tf.keras.optimizers.Nadam(learning_rate=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        model.compile(loss='categorical_crossentropy', optimizer=Nadam, metrics=['accuracy'])
        return model

    @staticmethod
    def __load_tokenizer(path):
        with open(path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        return tokenizer

    def getIntent(self, user_input):
        tokens = self.tokenizer.texts_to_sequences([user_input])
        tokens = pad_sequences(tokens, maxlen=6000)
        prediction = self.intentClassifier.predict(np.array(tokens))
        pred = np.argmax(prediction)
        classes = ['affirm_ready', 'affirm_hint', 'giving_answer', 'need_hint', 'affirm', 'decline', 'greetings']
        return classes[pred]
