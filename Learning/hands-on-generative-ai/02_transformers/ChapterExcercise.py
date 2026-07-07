from genaibook.core import get_device
device = get_device()
print(f"Using device: {device}")
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
def generate(model,tokenizer, input_ids, max_length=50, do_sample=False, top_k=None):
    