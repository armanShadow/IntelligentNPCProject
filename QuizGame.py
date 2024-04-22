from IntelligentNPC import IntelligentNPC
import re


class QuizMaster(IntelligentNPC):
    def __init__(self, name, questions_path,
                 conversation_template_str,
                 intent_model_path,
                 intent_tokenizer_path,
                 states,
                 rl_states):
        super().__init__(questions_path,
                         conversation_template_str,
                         intent_model_path,
                         intent_tokenizer_path,
                         states,
                         rl_states)

        self.name = name
        self.retrieval_input_variables = {}
        self.input_variables = {}

        self.current_question = ''
        self.question_template = ("randomly set the options\n" +
                                  "Category:\n" +
                                  "Difficulty:\n" +
                                  "Type:\n" +
                                  "Question:\n" +
                                  "Option A:\n" +
                                  "Option B:\n" +
                                  "Option C:\n" +
                                  "Option D:\n\n" +
                                  "What's your answer {player}?")

    def respond(self, user_input):
        self.input_variables.update({'user_input': user_input})
        user_intent = self.getIntent(user_input)
        print(user_intent)

        if user_intent == "greetings":
            response = self.greetings()

        elif user_intent == "giving_answer":
            response = self.provideFeedback()

        elif user_intent == "need_hint":
            response = self.informNumberOfHints()

        elif user_intent == "affirm":
            if self.getStates()['need_hint']:
                response = self.provideHint()
            else:
                response = self.askQuestion()

        elif user_intent == "affirm_ready":
            response = self.askQuestion()

        elif user_intent == "affirm_hint":
            response = self.provideHint()

        else:
            # user_intent == "decline"
            if self.getStates()['need_hint']:
                print('player does not want any help')
                self.updateStates({'need_hint': False})
                context = "the player deos not want any help. Continue with the quiz. do not skip the question."
                self.input_variables.update({"context": context})
                response = super().respond(self.input_variables)
            else:
                print('player not ready')
                context = "the player is not ready for the question."
                self.input_variables.update({"context": context})
                response = super().respond(self.input_variables)
            pass
        return response

    def greetings(self):
        print('action: greetings')
        context = ("Say hello to {player}, and introduce yourself. provide an intro to the quiz game and ask if the "
                   "player is ready to start the quiz.")
        self.input_variables.update({'context': context})
        return super().respond(self.input_variables)

    def selectQuestion(self):
        difficulty = self.getRLStates()['difficulty']
        self.retrieval_input_variables.update({"difficulty": difficulty, "asked": "false"})
        question = self.retrieve_docs(self.retrieval_input_variables)
        self.current_question = question[0].page_content
        self.deleteDocs(question)
        return question[0].page_content

    def askQuestion(self):
        print('action: askQuestion')
        question = self.selectQuestion()
        context = (f"given this template:\n{self.question_template}\n" +
                   f"ask the question below:\n{question}")
        self.input_variables.update({'context': context})
        return super().respond(self.input_variables)

    def provideFeedback(self):
        print('action: provideFeedback')
        context = (f"The player has given the answer for this question:\n{self.current_question}\n" 
                   "check the answer and provide feedback, then ask if "
                   "the player is ready for the next question")
        self.input_variables.update({'context': context})
        return super().respond(self.input_variables)

    def informNumberOfHints(self):
        print('action: informNumberOfHints')
        remaining_hints = self.getStates()['remaining_hints']
        if remaining_hints > 0:
            self.updateStates({"need_hint": True})
            context = ("The player is not sure what the correct answer is for this question:\n"
                       f"{self.current_question}\ninform that the player has {remaining_hints} remaining "
                       "hints for the whole game and ask if the player wants to use the hint option")
            self.input_variables.update({'context': context})
        else:
            context = ("The player is not sure what the correct answer is."
                       "inform the player ran out of the number of hints,"
                       " and the player should take a guess.")
            self.input_variables.update({'context': context})
        return super().respond(self.input_variables)

    def provideHint(self):
        print('action: provideHint')
        remaining_hints = self.getStates()['remaining_hints']
        self.updateStates({"need_hint": False})
        if remaining_hints > 0:
            self.updateStates({"remaining_hints": remaining_hints-1})
            context = ("The player is not sure what the correct answer is for this question:\n. "
                       f"{self.current_question}\nprovide a hint for the player")
            self.input_variables.update({'context': context})
        else:
            context = ("The player is not sure what the correct answer is."
                       "inform the player ran out of the number of hints, "
                       "and the player should take a guess.")
            self.input_variables.update({'context': context})
        return super().respond(self.input_variables)


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class QuizGame:
    def __init__(self, quiz_master, player):
        self.quiz_master = quiz_master
        self.quiz_master.input_variables.update({"quiz_master": quiz_master.name, "player": player.name})
        self.player = player
        self.currentQuestion = None

    def extractQuestion(self, raw_response):
        question = {"Category": None, "Difficulty": None, "Question": None, "Options": None, "isDetected": False}
        pattern = re.compile(
            """[\s\S]*Category: [\s\S]*Difficulty: [\s\S]*Type: [\s\S]*Question: [\s\S]*Option A: [\s\S]*Option B: [\s\S]*Option C: [\s\S]*Option D: [\s\S]*"""
        )
        match = pattern.match(raw_response)
        if match:
            category_index = raw_response.find("Category: ")
            difficulty_index = raw_response.find("Difficulty: ")
            type_index = raw_response.find("Type: ")
            question_index = raw_response.find("Question: ")
            option_a_index = raw_response.find("Option A: ")
            option_b_index = raw_response.find("Option B: ")
            option_c_index = raw_response.find("Option C: ")
            option_d_index = raw_response.find("Option D: ")
            end_index = raw_response[option_d_index:-1].find('\n') + option_d_index

            options = {"A": raw_response[option_a_index + 10:option_b_index - 1],
                       "B": raw_response[option_b_index + 10:option_c_index - 1],
                       "C": raw_response[option_c_index + 10:option_d_index - 1],
                       "D": raw_response[option_d_index + 10:end_index]}

            question = {"Category": raw_response[10 + category_index:difficulty_index - 1],
                        "Difficulty": raw_response[12 + difficulty_index:type_index - 1],
                        "Type": raw_response[6 + type_index:question_index - 1],
                        "Question": raw_response[10 + question_index:option_a_index - 1],
                        "Options": options,
                        "isDetected": True}

            self.currentQuestion = question

            response = raw_response[0:category_index] + raw_response[end_index:-1]
        else:
            response = raw_response
        return question, response
