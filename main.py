from QuizGame import Question, QuizMaster, QuizGame, Player
from GPT2Model import GPT2

if __name__ == '__main__':
    question1 = Question("What is the capital of France?", ["Paris", "Berlin", "Madrid", "Rome"], 1)
    question2 = Question("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Saturn"], 1)
    question3 = Question("What is the largest mammal in the world?",
                         ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], 2)

    # Create QuizMaster NPC and Player
    quizMaster_npc = QuizMaster("QuizMaster")
    player1 = Player("Player1")

    # Create QuizGame with questions, QuizMaster, and Player
    quiz_game = QuizGame(quizMaster_npc, [question1, question2, question3], player1)
    quiz_game.play_game()

