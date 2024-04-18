from ConversationalChatBot import ConversationalChatBot


class IntelligentNPC:
    def __init__(self, path, conversation_template_str, sample_conversation):
        self.conversational_model = ConversationalChatBot(path, conversation_template_str, sample_conversation)
        # we also may need these variables
        self.memory = None
        self.attention = None

    # We can introduce an abstract model of a human interaction here

    def decide(self):
        # here is the RL part
        pass

    def respond(self, user_input, stuff_input_variables, retrieval_input_variables):
        # here is the LLM part
        return self.conversational_model.generate_response(user_input, stuff_input_variables, retrieval_input_variables)
