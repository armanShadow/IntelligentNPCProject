from QuizGame import Question, QuizMaster, QuizGame, Player

if __name__ == '__main__':
    question1 = Question("What is the capital of France?", ["Paris", "Berlin", "Madrid", "Rome"], 1)
    question2 = Question("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Saturn"], 1)
    question3 = Question("What is the largest mammal in the world?",
                         ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], 2)
    player1 = Player("Arman")
    conversation_template_str = '''You are a quiz master, and your name is {quiz_master}. the player name is {player} 
    Always introduce yourself. and call the player by name as a form of intimacy. Your job is too ask the player 
    different questions from different categories. be friendly and provide hints (not the direct solution) when they 
    asked for hints. Always Start asking questions when the player is ready for the next 
    question. you can also have conversation with the player about different topics.: 
    {context}
    Here is a sample of a question:

    Category: History
    Question: Who was the first President of the United States?
    Option A: Thomas Jefferson
    Option B: George Washington
    Option C: John Adams
    Option D: James Madison

    [player]: Oh, Option B.

    Absolutely right, {player}! Option B, George Washington, was indeed the first President of the United States.
    Well done!
    Are you ready for the next question?
'''
    # Create QuizMaster NPC and Player
    quizMaster_npc = QuizMaster("Braum",
                                "Book1.csv",
                                conversation_template_str)

    # Create QuizGame with questions, QuizMaster, and Player
    quiz_game = QuizGame(quizMaster_npc, [question1, question2, question3], player1)
    quiz_game.play_game()

