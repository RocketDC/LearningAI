import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class CH1_PredictingProbabilities:
    """
    A class to demonstrate loading causal language models, running a forward pass,
    inspecting logits, finding the argmax, and applying softmax to convert logits to probabilities.
    """
    def __init__(self, model_name: str = "Qwen/Qwen2-0.5B"):
        """
        Loads the tokenizer and causal language model.
        AutoClasses dynamically select the correct classes under the hood
        (e.g., Qwen2TokenizerFast and Qwen2ForCausalLM).
        """
        print(f"Initializing model and tokenizer for '{model_name}'...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model_name = model_name

    def get_logits(self, prompt: str):
        """
        Runs a forward pass on the input prompt and returns input IDs and output logits.
        """
        # Tokenize prompt returning PyTorch tensors ("pt")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids
        
        # Forward pass (disable gradients for faster inference)
        with torch.no_grad():
            outputs = self.model(input_ids)
            
        return input_ids, outputs.logits

    def predict_next_token(self, prompt: str):
        """
        Uses argmax to find the single most likely next token predicted by the model.
        """
        _, logits = self.get_logits(prompt)
        final_logits = logits[0, -1] # Logits for the final token in the prompt
        
        best_token_id = final_logits.argmax().item()
        decoded_token = self.tokenizer.decode(best_token_id)
        
        print("\n--- Next Token Prediction (Argmax) ---")
        print(f"Argmax Token ID: {best_token_id}")
        print(f"Decoded Next Token: {repr(decoded_token)}")
        return best_token_id, decoded_token

    def predict_top_k_probabilities(self, prompt: str, k: int = 10):
        """
        Applies softmax to raw logits to convert them to probabilities,
        and prints the top k predicted next tokens along with their probability percentages.
        """
        _, logits = self.get_logits(prompt)
        final_logits = logits[0, -1] # Logits for the final token in the prompt
        
        # Convert logits into probability distribution using Softmax normalization
        probabilities = final_logits.softmax(dim=0)
        
        # Extract the top k probability values and their corresponding indices
        top_k = torch.topk(probabilities, k)
        
        print(f"\n--- Top {k} Predicted Next Tokens (with Softmax Probabilities) ---")
        for i, (val, idx) in enumerate(zip(top_k.values, top_k.indices)):
            token_id = idx.item()
            token_str = self.tokenizer.decode(token_id)
            prob_percent = val.item()
            print(f"  {i+1:<2}. Token ID: {token_id:<6} -> Decoded: {repr(token_str):<12} | Probability: {prob_percent:.2%}")
            
        return top_k

    def run_all_experiments(self, prompt: str):
        """
        Runs a full suite of experiments: printing logits shape, argmax prediction,
        and top 10 probabilities.
        """
        input_ids, logits = self.get_logits(prompt)
        
        print(f"\n=================== Running Experiments: {self.model_name} ===================")
        print(f"Prompt: \"{prompt}\"")
        print(f"Input IDs shape (batch_size, seq_len): {input_ids.shape}")
        print(f"Logits shape (batch_size, seq_len, vocab_size): {logits.shape}")
        
        # 1. Argmax prediction
        self.predict_next_token(prompt)
        
        # 2. Probability analysis
        self.predict_top_k_probabilities(prompt, k=10)

if __name__ == "__main__":
    prompt = "It was a dark and stormy"
    
    # Initialize predictor
    predictor = CH1_PredictingProbabilities("Qwen/Qwen2-0.5B")
    
    # Run all experiments
    predictor.run_all_experiments(prompt)
