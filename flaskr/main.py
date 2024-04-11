from QuizGame import QuizMaster, QuizGame, Player
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()

player1 = Player("Arman")

conversation_template_str = '''You are a quiz master, and your name is {quiz_master}. the player name is {player} 
        Always introduce yourself. and call the player by name as a form of intimacy. Your job is too ask the player 
        different questions from different categories. be friendly and provide hints (not the direct solution) when they 
        asked for hints. Always Start asking questions when the player is ready for the next 
        question. you can also have conversation with the player about different topics.: 
        {context}
        Here is a sample of a question:

        Category: History 
        Difficulty: Easy
        Type: Multiple Choice
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
                            "https://opentdb.com/api.php?amount=10&type=multiple",
                            conversation_template_str)

# Create QuizGame with questions, QuizMaster, and Player
quiz_game = QuizGame(quizMaster_npc, player1)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    # Get user input from the form
    data = request.form
    user_input = data['user_input']
    bot_response = quiz_game.quiz_master.respond(user_input, quiz_game.quiz_master.input_variables)
    return {'Response': bot_response}


@app.route('/chatHistory', methods=['GET'])
def getChatHistory():
    chat_history = quiz_game.quiz_master.conversational_model.getChatHistoryString()
    return {'ChatHistory': chat_history}


if __name__ == '__main__':
    app.run(debug=True)
