from ConversationalChatBot import ConversationalChatBot
from DialogueManager import DialogueManager
from Qtable import Qtable


class IntelligentNPC:
    def __init__(self, path,
                 conversation_template_str,
                 model_path,
                 tokenizer_path,
                 q_table_path,
                 states,
                 rl_states):
        self.conversational_model = ConversationalChatBot(path, conversation_template_str)
        self.dialogueManager = DialogueManager(model_path, tokenizer_path, states, rl_states)
        self.q_table = Qtable(q_table_path)

    def respond(self, input_variables, context):
        input_variables.update({"context": context})
        return self.conversational_model.generate_response(input_variables)

    def retrieve_docs(self, retrieval_input_variables):
        retrieved_docs = self.conversational_model.retrieve_docs(retrieval_input_variables)
        return retrieved_docs

    def deleteDocs(self, docs):
        self.conversational_model.deleteDocs(docs)

    def getIntent(self, user_input):
        return self.dialogueManager.getIntent(user_input)

    def updateStates(self, states):
        self.dialogueManager.state_tracker.updateStates(states)

    def updateRLStates(self, rl_states):
        self.dialogueManager.state_tracker.updateRLStates(rl_states)

    def getRLStates(self):
        return self.dialogueManager.state_tracker.getRLStates()

    def getStates(self):
        return self.dialogueManager.state_tracker.getStates()

    def getAction(self, rl_states):
        return self.q_table.getAction(rl_states)
