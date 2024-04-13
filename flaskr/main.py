from QuizGame import QuizMaster, QuizGame, Player
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()

player1 = Player("Arman")

conversation_template_str = '''You are a quiz master, and your name is {quiz_master}. the player name is {player} 
Always introduce yourself. and call the player by name as a form of intimacy. Your job is too ask the player 
different questions from the given set of questions. do not improvise any questions. be friendly and provide hints ( 
not the direct solution) when they asked for hints. Always ask the player if she or he is ready for the next 
question. you can also have conversation with the player about different topics.

{context}

always show the question with the exact given template at the end of your response when you are asking the question (
do not change the template). always provide an intro related to the question to enthuse the player while you are 
asking the question. here is the template:

Category: History
Difficulty: Easy
Type: Multiple Choice
Question: Who was the first President of the United States?
Option A: Thomas Jefferson
Option B: George Washington
Option C: John Adams
Option D: James Madison

What's your answer, {player}".

[player]: Oh, Option B. [other possible responses: I think the answer is George Washington, The answer is B]

Absolutely right, {player}! Option B, George Washington, was indeed the first President of the United States.
Well done!
Are you ready for the next question?'''

quizMaster_npc = QuizMaster("Braum",
                            "./questions.json",
                            conversation_template_str)

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
    question, filtered_response = quiz_game.extractQuestion(bot_response)
    return {'Response': filtered_response, "Question": question}


@app.route('/chatHistory', methods=['GET'])
def getChatHistory():
    chat_history = quiz_game.quiz_master.conversational_model.getChatHistoryString()
    filtered_chat_history = []
    for message in chat_history:
        if message['type'] == "AIMessage":
            question, filtered_response = quiz_game.extractQuestion(message['content'])
            message['content'] = {'Response': filtered_response, "Question": question}

    return {'ChatHistory': chat_history}


@app.route('/getQuestion', methods=['GET'])
def getQuestion():
    question = quiz_game.currentQuestion
    return {'currQuestion': question}


if __name__ == '__main__':
    app.run(debug=True)
