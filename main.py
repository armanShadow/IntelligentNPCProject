from transformers import BertTokenizer, BertModel
from transformers import pipeline, set_seed

if __name__ == '__main__':
    bertTokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bertModel = BertModel.from_pretrained("bert-base-uncased")
    text = "Replace me by any text you'd like."
    encoded_input = bertTokenizer(text, return_tensors='pt')
    output = bertModel(**encoded_input)

    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    out = generator("The White man worked as a",truncation=True, max_length=10, num_return_sequences=5)
    print(out)
