import os

from langchain_core.messages import HumanMessage, AIMessage

from QuizGame import QuizMaster, QuizGame, Player
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response
from SpeechTextTranslator import SpeechTextTranslator as stt

app = Flask(__name__)
load_dotenv()

player1 = Player("Arman")

conversation_template_str = '''You are a quiz master, and your name is {quiz_master}. the player name is {player}. 
Your job is too ask the player the given question. be friendly and provide hints (not the direct solution) when they 
asked for hints. Always ask the player if she or he is ready for the next question then proceed to the next question. 
you can also have conversation with the player about different topics. always show the question with the exact given 
template below when you are asking the question.

Here is the given question you should ask:
{context}

here is the template for asking:

Here is your question:
(randomly set the options)
Category:
Difficulty:
Type:
Question:
Option A:
Option B:
Option C:
Option D:

What's your answer {player}?
'''

sample_conversation = [HumanMessage(content="Hey"),
                       AIMessage(content="Hi {player}, my name is {quiz_master}. Are you Ready for a fun quiz?"),
                       HumanMessage(content="Yes!"),
                       AIMessage(content="Great, here is the first question: {context}\n What's your answer {player}"),
                       ]

quizMaster_npc = QuizMaster("Braum",
                            "./questions2.json",
                            conversation_template_str,
                            sample_conversation)

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
    quiz_game.quiz_master.retrieval_input_variables.update({"difficulty": "easy", "asked": "false"})
    bot_response = quiz_game.quiz_master.respond(user_input, quiz_game.quiz_master.stuff_input_variables,
                                                 quiz_game.quiz_master.retrieval_input_variables)
    path = stt.translate_text_to_speech(bot_response)
    file_name = os.path.basename(path).split('/')[-1]
    question, filtered_response = quiz_game.extractQuestion(bot_response)
    return {'Response': filtered_response, "Question": question, "TranslatedSpeechFile": file_name}


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
