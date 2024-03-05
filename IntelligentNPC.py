from transformers import BertTokenizer, BertModel
from GPT2Model import GPT2


class IntelligentNPC:
    def __init__(self):
        # NLP
        self.bertModel = BertModel.from_pretrained("bert-base-uncased")
        self.bertTokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # LLM
        self.llm = GPT2()
        # we also may need these variables
        self.memory = None
        self.attention = None

    # We can introduce an abstract model of a human interaction here

    def listen(self, response):
        # here is the NLP part
        pass

    def decide(self):
        # here is the RL part
        pass

    def talk(self, prompt):
        # here is the LLM part
        return self.llm.generate_text(prompt)
