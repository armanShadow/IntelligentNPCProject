import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from QuizGameSimulator import QuizGame

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.4, epsilon=0.4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((str(state), action), 0.0)

    def choose_action(self, state, available_actions):
        if np.random.random() < self.epsilon:
            return np.random.choice(available_actions)
        else:
            q_values = [self.get_q_value(str(state), action) for action in available_actions]
            return available_actions[np.argmax(q_values)]

    def update_q_value(self, state, action, reward, next_state, available_actions):
        old_q_value = self.get_q_value(str(state), action)
        future_q_values = [self.get_q_value(str(next_state), next_action) for next_action in available_actions]
        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (reward + self.gamma * max(future_q_values))
        self.q_table[(str(state), action)] = new_q_value

game = QuizGame()
agent = QLearningAgent()
num_episodes = 4000

rewards = []
iter = 1
for episode in range(num_episodes):
    state = game.reset()
    done = False
    total_reward = 0
    while not done:
        action = agent.choose_action(state, game.actions)
        next_state, reward, done = game.step(action)
        agent.update_q_value(state, action, reward, next_state, game.actions)
        #print('Current State: ', state, "\t Current action: ", action, "\t Reward: ", reward, "\t Next State: ", next_state)
        total_reward += reward
        state = next_state
        if iter == 15:
            done = True
        iter+=1
    rewards.append(total_reward)

# Calculate running average
running_avg_reward = np.cumsum(rewards) / (np.arange(num_episodes) + 1)

# Convert the Q-table into a DataFrame
q_table_df = pd.DataFrame(list(agent.q_table.items()), columns=['State_Action', 'Q_Value'])
# Split the State_Action column into separate State and Action columns
q_table_df[['State', 'Action']] = pd.DataFrame(q_table_df['State_Action'].tolist(), index=q_table_df.index)
# Remove the State_Action column
q_table_df = q_table_df.drop(columns=['State_Action'])
# Convert the State tuples to strings and remove brackets and quotes
q_table_df['State'] = q_table_df['State'].apply(lambda x: str(x).replace("(", "").replace(")", "").replace("'", ""))
# Sort the DataFrame by Q_Value in descending order
q_table_df = q_table_df.sort_values(by='Q_Value', ascending=False)
# Save the DataFrame to a CSV file
q_table_df.to_csv('./data/q_table_Qlearning.csv', index=False)

# Plot running average reward
plt.plot(running_avg_reward)
plt.title('Running Average Reward')
plt.xlabel('Episode')
plt.ylabel('Average Reward')
plt.savefig("./data/Learning Curve Q-Learning")



