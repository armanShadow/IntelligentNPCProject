import random

class QuizGame:
    def __init__(self):
        self.state_space = ['random_conversation', 'easy', 'medium', 'hard', 'end']
        self.action_space = ['ask_easy', 'ask_medium', 'ask_hard', 'respond', 'end_game']
        self.state = 'easy'
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.score = 0
        self.consecutive_correct = 0

    def step(self, action):
        if action == 'end_game':
            self.state = 'end'
            return self.state, self.score, True

        if action.startswith('ask_'):
            difficulty = action.split('_')[1]
            if difficulty == self.state:
                if random.random() < 0.5:  # 50% chance of correct answer
                    self.correct_answers += 1
                    self.consecutive_correct += 1
                    self.score += {'easy': 2, 'medium': 4, 'hard': 6}[difficulty]
                    if self.consecutive_correct == {'easy': 3, 'medium': 2, 'hard': 1}[difficulty]:
                        self.state = {'easy': 'medium', 'medium': 'hard', 'hard': 'end'}[difficulty]
                        self.consecutive_correct = 0
                else:
                    self.incorrect_answers += 1
                    if self.incorrect_answers == 2:
                        self.state = 'end'
            else:
                self.state = 'random_conversation'

        if action == 'respond':
            if self.state == 'random_conversation':
                self.state = 'easy'

        return self.state, self.score, self.state == 'end'

    def reset(self):
        self.state = 'easy'
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.score = 0
        self.consecutive_correct = 0
        return self.state
