from transformers import AutoTokenizer

class CH1_AutoTokenizer:
    """
    A custom tokenizer class for Chapter 1 exercises, wrapping Hugging Face's AutoTokenizer.
    """
    def __init__(self, model_name: str = "Qwen/Qwen2-0.5B"):
        """
        Initializes the tokenizer with a pre-trained model.
        """
        print(f"Initializing tokenizer from '{model_name}'...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model_name = model_name

    def tokenize(self, prompt: str):
        """
        Tokenizes the prompt and returns input IDs.
        """
        return self.tokenizer(prompt).input_ids

    def print_tokens(self, input_ids):
        """
        Decodes and prints each token ID and its matching string representation.
        """
        print("\nToken ID and String mappings:")
        for t in input_ids:
            print(f"{t}\t: {self.tokenizer.decode(t)}")

    def process(self, prompt: str):
        """
        Helper method to run tokenization, print input IDs, and print token mappings.
        """
        print(f"\nPrompt: \"{prompt}\"")
        input_ids = self.tokenize(prompt)
        print(f"Input IDs: {input_ids}")
        self.print_tokens(input_ids)
        return input_ids

if __name__ == "__main__":
    # Test execution
    prompt = "It was dark and stormy"
    
    # Initialize the tokenizer wrapping Qwen2-0.5B
    tokenizer_wrapper = CH1_AutoTokenizer("Qwen/Qwen2-0.5B")
    
    # Process prompt
    tokenizer_wrapper.process(prompt)
