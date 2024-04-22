import random

class QuizGame:
    def __init__(self):
        self.levels = ['easy', 'medium', 'hard']
        self.actions = ['ask_easy', 'ask_medium', 'ask_hard', 'end_game']
        self.state = (self.levels[0], 0, 0)  # Start at easy level with no correct or incorrect answers

    def step(self, action):
        reward = 0
        done = False
        level, correct, incorrect = self.state
        print('current state: ', self.state, action)

        rand_val = random.random()
        if rand_val < 0.5 :  # 50% chance of correct answer by the user
            correct += 1
        else:
            incorrect += 1
        if correct <=7 and incorrect <=2:
            if correct <= 3 and action == 'ask_easy':
                level = "easy"
                reward += 20
            elif correct > 3 and correct <= 5 and action == 'ask_medium':
                level = "medium"
                reward += 20
            elif correct >= 5 and correct < 6 and action == 'ask_hard':
                level = "hard"
                reward += 20
            elif correct == 7 and action == 'end_game' and level == 'hard':
                correct-=1
                reward += 30
            else:
                reward-=20

        if correct > 6 or incorrect > 2:
            reward-=20
            done = True

        self.state = (level, correct, incorrect)
        print('next_state: ',  self.state, 'Reward: ', reward)
        
        return self.state, reward, done

    def reset(self):
        # Reset the game to the initial state
        self.state = (self.levels[0], 0, 0)
        return self.state
