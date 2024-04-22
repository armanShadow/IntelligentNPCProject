import os

from QuizGame import QuizMaster, QuizGame, Player
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response
from SpeechTextTranslator import SpeechTextTranslator as stt

app = Flask(__name__)
load_dotenv()

player1 = Player("Arman")

conversation_template_str = '''You are a quiz master, and your name is {quiz_master}. the player name is {player}. 
Your job is to perform only and only the action in the given context. be nice and friendly.

Here is the given context:
{context}
'''


states = {"ready": False,
          "need_hint": False,
          "remaining_hints": 2,
          "out_of_scope": False,
          "waiting_for_answer": False,
          "giving_answer": False}

rl_states = {"difficulty": "easy",
             "consecutive_number": 0,
             "incorrect_answers": 0,
             "need_hint": False,
             "number_of_hints": 0
             }

quizMaster_npc = QuizMaster("Braum",
                            "data/questions2.json",
                            conversation_template_str,
                            'models/Intent_Classification.keras',
                            'utils/tokenizer.pkl',
                            states,
                            rl_states)

quiz_game = QuizGame(quizMaster_npc, player1)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/output.wav')
def stream_wav():
    def generate():
        with open("output.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

    return Response(generate(), mimetype="audio/x-wav")


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    # Get user input from the form
    data = request.form
    user_input = data['user_input']

    bot_response = quiz_game.quiz_master.respond(user_input)

    #path = stt.translate_text_to_speech(bot_response)
    #file_name = os.path.basename(path).split('/')[-1]

    question, filtered_response = quiz_game.extractQuestion(bot_response)

    return {'Response': filtered_response, "Question": question, "TranslatedSpeechFile": 'output.wav'}


@app.route('/chatHistory', methods=['GET'])
def getChatHistory():
    chat_history = quiz_game.quiz_master.conversational_model.getChatHistoryString()
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
