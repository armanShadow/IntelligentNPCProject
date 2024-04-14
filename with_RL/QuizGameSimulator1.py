import random

class QuizGame:
    def __init__(self):
        self.states = ['S_easy', 'S_medium', 'S_hard', 'S_end']
        self.state_mapping = {'S_easy' : 0, 'S_medium' : 1, 'S_hard' : 2, 'S_end' : 3}
        self.actions = ['A_answer_question', 'A_random_conversation']
        self.state = 'S_easy'
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.score = 0

    def transition(self, action):
        if action == 'A_answer_question':
            # Assume a 50% chance of answering correctly
            if random.random() < 0.5:
                self.correct_answers += 1
                if self.state == 'S_easy' and self.correct_answers == 6:
                    self.state = 'S_medium'
                    self.correct_answers = 0
                elif self.state == 'S_medium' and self.correct_answers == 4:
                    self.state = 'S_hard'
                    self.correct_answers = 0
            else:
                self.incorrect_answers += 1
                if self.incorrect_answers == 3:
                    self.state = 'S_end'

    def reward_function(self, action):
        print(self.state)
        if self.state == 'S_end':
            return 0
        elif action == 'A_answer_question':
            if self.state == 'S_easy':
                return 2
            elif self.state == 'S_medium':
                return 4
            elif self.state == 'S_hard':
                return 6
        elif action == 'A_random_conversation':
            return 0  # No reward for random conversation

    def step(self, action):
        self.transition(action)
        reward = self.reward_function(action)
        print("action and reward: ", action, reward)
        self.score += reward
        return self.state, reward, self.score

    def reset(self):
        self.state = 'S_easy'
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.score = 0

    def simulate(self):
        self.reset()
        while self.state != 'S_end':
            action = random.choice(self.actions)
            state, reward, score = self.step(action)
            print(f"Action: {action}, New State: {state}, Reward: {reward}, Total Score: {score}")

# Create a QuizGame instance and simulate a game
#game = QuizGame()
#game.simulate()
