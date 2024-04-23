# IntelligentNPCProject
Intelligent NPCs in Video Games using RL, LLM and NLP models
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(len(tokenizer.word_index) + 1, embed_dim),
    tf.keras.layers.LSTM(lstm_num, dropout=0.1, kernel_regularizer=regularizers.L2(0.001)),
    tf.keras.layers.Dense(lstm_num, activation='relu', kernel_regularizer=regularizers.L2(0.001)),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(output_dim, activation='softmax')
])