from IntelligentNPC import IntelligentNPC


class QuizMaster(IntelligentNPC):
    def __init__(self, name, questions_url, conversation_template_str):
        super().__init__(questions_url, conversation_template_str)
        self.name = name
        self.input_variables = None

    def selectQuestion(self, questions):
        pass

    def askQuestion(self, question):
        pass

    def provide_feedback(self):
        pass

    def provide_hint(self):
        pass


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class QuizGame:
    def __init__(self, quiz_master, player):
        self.quiz_master = quiz_master
        self.quiz_master.input_variables = {"quiz_master": quiz_master.name, "player": player.name}
        self.player = player


