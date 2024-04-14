from QuizGameSimulator import QuizGame
import numpy as np
import pandas as pd

class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.8, epsilon=0.3):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, available_actions):
        if np.random.random() < self.epsilon:
            return np.random.choice(available_actions)
        else:
            q_values = [self.get_q_value(state, action) for action in available_actions]
            return available_actions[np.argmax(q_values)]

    def update_q_value(self, state, action, reward, next_state, available_actions):
        old_q_value = self.get_q_value(state, action)
        future_q_values = [self.get_q_value(next_state, next_action) for next_action in available_actions]
        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (reward + self.gamma * max(future_q_values))
        self.q_table[(state, action)] = new_q_value



game = QuizGame()
agent = QLearningAgent()

for episode in range(100000):
    state = game.reset()
    done = False

    while not done:
        action = agent.choose_action(state, game.action_space)
        next_state, reward, done = game.step(action)
        agent.update_q_value(state, action, reward, next_state, game.action_space)
        #print('Current State: ', state, "\t Current action: ", action, "\t Reward: ", reward, "\t Next State: ", next_state)
        state = next_state
        
    #print(f"Episode {episode + 1} finished with score {game.score}")

# Convert the Q-table into a DataFrame
q_table_df = pd.DataFrame(list(agent.q_table.items()), columns=['State_Action', 'Q_Value'])
q_table_df.to_csv('./data/q_table.csv', index=False)
