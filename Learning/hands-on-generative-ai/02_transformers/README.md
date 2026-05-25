# Chapter 02: Transformers

This chapter covers the foundational architecture of the modern AI revolution: the Transformer. We explore self-attention, multi-head attention, positional encoding, and the difference between encoder-only, decoder-only, and encoder-decoder architectures.

---

## 🔑 Key Concepts
*   **The Self-Attention Mechanism**
*   **Positional Encodings**
*   **Encoder-Only (BERT) vs. Decoder-Only (GPT) vs. Seq2Seq (T5, BART)**
*   **Tokenization and Vocabulary**

---

## 📓 Notebook
*   **Local Notebook:** [02_transformers.ipynb](./02_transformers.ipynb)
*   **Colab Notebook:** [Launch on Google Colab](https://colab.research.google.com/github/genaibook/genaibook/blob/main/chapter2.ipynb)

---

## 🔤 Tokenizing Text

Tokenization is the critical first step in any transformer pipeline. We process an input string (the *prompt*) through a tokenizer to **encode** it into a sequence of integer token IDs, representing individual tokens. These IDs can then be **decoded** back into human-readable text.

### Example Experiment

Using `Qwen/Qwen2-0.5B` to tokenize the prompt `"It was dark and stormy"`:

*   **Prompt**: `"It was dark and stormy"`
*   **Encoded Input IDs**: `[2132, 572, 6319, 323, 13458, 88]`

#### Token ID and String Mappings:
| Token ID | Decoded Token |
| :---: | :--- |
| **2132** | `It` |
| **572** | ` was` |
| **6319** | ` dark` |
| **323** | ` and` |
| **13458** | ` storm` |
| **88** | `y` |

### Key Observations & Takeaways

> [!IMPORTANT]
> 1. **Subword Tokenization:** In this mapping, the word `"stormy"` was split into two tokens: `" storm"` (ID `13458`) and `"y"` (ID `88`). Tokenizers split words into subwords to efficiently handle vocabulary size and represent out-of-vocabulary words. Some of the most popular subword tokenization approaches include:
>    *   **Byte-level Byte-Pair Encoding (BPE):** Used by models like GPT-2, GPT-4, and Qwen.
>    *   **WordPiece:** Used by models like BERT.
>    *   **SentencePiece:** Used by models like T5 and LLaMA.
> 2. **Model-Specific Tokenizers:** Every model is trained with a unique vocabulary and tokenization scheme. It is critical to select and load the correct tokenizer matching your specific model (e.g., using `AutoTokenizer.from_pretrained(model_name)`), otherwise the token IDs will map incorrectly and degrade the model's performance.

---

## 🎲 Predicting Probabilities

Causal language models (such as GPT-2, Qwen, and SmolLM) are **autoregressive** models. They are pre-trained on a self-supervised task: predicting the next token in a sequence given all preceding tokens.

### Loading Models via AutoClasses

The Hugging Face `transformers` library supports hundreds of model architectures. Rather than importing model-specific classes manually (e.g., `Qwen2ForCausalLM` or `Qwen2TokenizerFast`), we use **AutoClasses** (such as `AutoModelForCausalLM` and `AutoTokenizer`). The library dynamically instantiates the correct architecture under the hood based on the configuration of the model we select.

Common AutoModel classes based on tasks include:
*   `AutoModelForCausalLM` (Next-token prediction / text generation)
*   `AutoModelForSequenceClassification` (Sentiment analysis / sequence classification)
*   `AutoModelForObjectDetection` (Object detection in images)

Under the hood for our model (`Qwen/Qwen2-0.5B`), `transformers` automatically resolves to a **`Qwen2TokenizerFast`** tokenizer and a **`Qwen2ForCausalLM`** model class.

### Extracting Logits

To inspect the raw prediction values (logits) for the next token:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-0.5B")

# 2. Tokenize prompt returning PyTorch tensors
prompt = "It was a dark and stormy"
inputs = tokenizer(prompt, return_tensors="pt")
input_ids = inputs.input_ids

# 3. Forward pass to get outputs containing logits
with torch.no_grad():
    outputs = model(input_ids)

# 4. Check the logits shape
print(outputs.logits.shape)  # Output: torch.Size([1, 7, 151936])
```

#### Logits Dimension Breakdown `[batch_size, sequence_length, vocab_size]`:
- **`batch_size` (1)**: The number of sequences processed in parallel.
- **`sequence_length` (7)**: The number of input tokens in our prompt (`"It was a dark and stormy"`).
- **`vocab_size` (151936)**: The vocabulary size of `Qwen2`. For each position in the prompt, the model calculates a logit score for every token in its vocabulary.

### 🎯 Identifying the Most Likely Next Token (Argmax)

To find the single most likely token predicted by the model for the next position, we extract the logits corresponding to the last token in our sequence (`[0, -1]`), find the index with the maximum score using `argmax()`, and decode that token ID:

```python
# Extract logits for the last token in the sequence
final_logits = outputs.logits[0, -1]

# Get the token ID with the highest score
best_token_id = final_logits.argmax().item()

# Decode the ID back to a human-readable string
print(tokenizer.decode(best_token_id))  # Output: ' night'
```

### 🧠 Self-Attention: The Core Engine

How does the model understand that `' night'` makes the most sense after `"It was a dark and stormy"`?
*   **The Self-Attention Mechanism:** This is the core building block of the Transformer architecture.
*   **Intuition:** Self-attention allows the model, at each generation step, to evaluate and weigh the relationship between every token in the prompt (e.g., how `"stormy"` connects with `"dark"`, `"was"`, and `"a"`). This enables the model to identify how much each token contributes to the overall contextual meaning of the sequence, allowing it to predict appropriate next-word probabilities.

### 📈 Normalizing Logits to Probabilities (Softmax)

Raw logits are unbounded real numbers, representing unnormalized prediction scores. To interpret how confident the model is in its predictions, we must convert these scores into a probability distribution.

This is done using the **`softmax()`** operation, which:
1.  **Exponentiates** each value (ensuring they are all positive numbers).
2.  **Normalizes** the values by dividing each by the sum of all exponentiated values.
3.  As a result, all values are mapped between `0` and `1` (`0%` to `100%`) and their sum is exactly `1.0`.

To find and display the top 10 next-token predictions with their respective confidence percentages:

```python
import torch

# Apply softmax across the vocabulary dimension (dim=0)
probabilities = final_logits.softmax(dim=0)

# Fetch the top 10 tokens and their probabilities
top10 = torch.topk(probabilities, 10)

# Print decoded tokens along with their formatted percentage scores
for value, index in zip(top10.values, top10.indices):
    token_str = tokenizer.decode(index)
    print(f"{repr(token_str):<12} : {value.item():.2%}")
```

---

## 🛠️ Suggestions & Exercises
1. Follow along with the book's chapter text and complete the cells in the notebook.
2. Complete the exercises at the end of the chapter to test your knowledge.

