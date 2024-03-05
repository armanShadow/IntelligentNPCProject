from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GPT2:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2-large", pad_token_id=self.tokenizer.eos_token_id)
        self.model.eval()

    def generate_text(self, prompt, max_length=100, temperature=0.7, top_k=50):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        output = self.model.generate(
            input_ids,
            top_k=top_k,
            top_p=0.95,
            temperature=temperature,
            max_length=max_length,
            early_stopping=True,
            no_repeat_ngram_size=2,
            num_beams=5,
            do_sample=True
        )
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text
