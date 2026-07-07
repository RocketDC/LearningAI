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

## ✍️ Generating Text

Once we have mapped input strings to token IDs, we can feed them into the model to generate a sequence of new tokens. There are different decoding strategies to predict and select these subsequent tokens.

### 1. Greedy Decoding

Greedy decoding is the most straightforward generation strategy. At each step, the model selects the next token with the absolute highest probability (the logit argmax).

#### Python Implementation:
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-0.5B")

# 2. Encode input prompt to get PyTorch tensors (Input IDs)
prompt = "It was a dark and stormy"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# 3. Generate tokens using Greedy Decoding (default behavior)
output_ids = model.generate(input_ids, max_new_tokens=20)

# 4. Decode the generated token IDs back to a human-readable string
decoded_text = tokenizer.decode(output_ids[0])

print("Input IDs: ", input_ids[0].tolist())
print("Output IDs:", output_ids[0].tolist())
print(f"Generated text: {decoded_text}")
```

#### Outputs from our run:
```text
Input IDs:  [2132, 572, 264, 6319, 323, 13458, 88]
Output IDs: [2132, 572, 264, 6319, 323, 13458, 88, 3729, 13, 576, 12884, 572, 6319, 323, 279, 9956, 572, 1246, 2718, 13, 576, 11174, 572, 50413, 1495, 323, 279]
Generated text: It was a dark and stormy night. The sky was dark and the wind was howling. The rain was pouring down and the
```

#### Limitation of Greedy Decoding:
> [!WARNING]
> Greedy decoding selects the next word one-by-one based purely on the immediate highest local probability. While fast, this greedy selection can lead to repetitive phrasing or sub-optimal text because it does not consider the long-term probability of the sentence as a whole (a locally optimal token at step $t$ might lead to very low probability options at step $t+1$).

---

### 2. Beam Search

Beam Search addresses the short-sighted nature of greedy decoding by looking at the cumulative probability of whole sentences rather than just the next step.

*   Instead of keeping only the single best token at each step, Beam Search maintains a fixed number of candidate sequences (known as the **beam width** or number of beams, $B$).
*   At each generation step, it tracks and evaluates the overall joint probability of all active paths.
*   By assessing the probability of the entire sequence, Beam Search finds a globally more probable and coherent output.

#### Python Implementation:
```python
# Generate text using Beam Search (specifying num_beams)
beam_output = model.generate(input_ids, num_beams=5, max_new_tokens=30)
decoded_beam_text = tokenizer.decode(beam_output[0])

print("Beam Output IDs:", beam_output[0].tolist())
print(f"Generated text: {decoded_beam_text}")
```

#### Outputs from our run:
```text
Beam Output IDs: [2132, 572, 264, 6319, 323, 13458, 88, 3729, 13, 576, 9956, 572, 1246, 2718, 11, 323, 279, 11174, 572, 50413, 1495, 13, 576, 12884, 572, 6319, 323, 13701, 5533, 11, 323, 279, 3720, 572, 10199, 448, 279]
Generated text: It was a dark and stormy night. The wind was howling, and the rain was pouring down. The sky was dark and gloomy, and the air was filled with the
```

> [!TIP]
> **Greedy vs. Beam Search Comparison:** 
> * **Greedy:** `...night. The sky was dark and the wind was howling. The rain was pouring down and the`
> * **Beam Search:** `...night. The wind was howling, and the rain was pouring down. The sky was dark and gloomy, and the air was filled with the`
> 
> Beam Search structures the clauses much more naturally, utilizing commas and avoiding the repetition of `"dark"` immediately after starting the next sentence, leading to a much higher quality generation.

### 🎛️ Controlling Generation: Repetition Penalty & Banned Words

To fine-tune the generation process further, we can use parameters that penalize repetitions or ban specific words from appearing in the generated text.

#### 1. Repetition Penalty (`repetition_penalty`)
*   **What it does:** Penalizes tokens that have already been generated, steering the model away from repetitive phrases or loops.
*   **Settings:** A value of `1.0` means no penalty. Values greater than `1.0` (e.g., `2.0`) discourage repetition, encouraging more creative and varied word choices.

#### 2. Banned Words (`bad_words_ids`)
*   **What it does:** Explicitly prevents specific sequences of tokens from being generated.
*   **Settings:** Accepts a list of lists of token IDs (e.g., `[[token_id_1], [token_id_2, token_id_3]]`).
*   **Tokenizer Catch:** Because tokenizers treat words with a leading space (e.g., `" night"`, ID `3729`) differently than words without one (e.g., `"night"`, ID `9287`), it is important to include **both** token IDs in the banned list to block a word completely.

#### Python Implementation:
```python
# 1. Define bad words to ban (banning both "night" and " night")
bad_words = ["night", " night"]
bad_words_ids = tokenizer(bad_words, add_special_tokens=False).input_ids

# 2. Generate text using Beam Search with repetition penalty and banned words
beam_output = model.generate(
    input_ids,
    num_beams=5,
    repetition_penalty=2.0,
    bad_words_ids=bad_words_ids,
    max_new_tokens=38
)
decoded_text = tokenizer.decode(beam_output[0])

print("Banned word token IDs:", bad_words_ids)
print("Output IDs:", beam_output[0].tolist())
print(f"Generated text: {decoded_text}")
```

#### Outputs from our run:
```text
Banned word token IDs: [[9287], [3729]]
Output IDs: [2132, 572, 264, 6319, 323, 13458, 88, 11458, 304, 220, 17, 15, 16, 18, 13, 358, 38726, 705, 311, 279, 5112, 315, 11174, 19558, 279, 15134, 315, 847, 13154, 4752, 13, 1084, 572, 83253, 19423, 323, 12590, 11, 323, 358, 1030, 902, 4522, 1128, 311]
Generated text: It was a dark and stormy evening in 2013. I woke up to the sound of rain hitting the roof of my apartment building. It was raining cats and dogs, and I had no idea what to
```
*Note: Since the word `"night"` (both `"night"` and `" night"`) was fully banned, the model chose the next most probable token, which was `" evening"`.*

---

## 🛠️ Suggestions & Exercises
1. Follow along with the book's chapter text and complete the cells in the notebook.
2. Complete the exercises at the end of the chapter to test your knowledge.

## Zero-Shot Generalization

Zero-shot generalization refers to a model's ability to make predictions or perform a task without being explicitly trained for that specific scenario or workflow. Instead of memorizing exact patterns, the model leverages the knowledge and relationships it learned during training to infer outcomes for unseen situations.

In Generative AI and Transformers, zero-shot generalization enables a model to solve tasks it has never directly encountered by understanding context and learned language patterns.

For example, a language model can classify whether a movie review is positive or negative even when it has not been specifically trained on a sentiment classification pipeline. It predicts the outcome by interpreting the prompt and evaluating token probabilities.

### Example: Sentiment Classification Using Prompting

```python
# Token IDs for sentiment labels
tokenizer.encode(" positive"), tokenizer.encode(" negative")


def score(review):
    """
    Predict whether a review is positive or negative.

    This function predicts sentiment using prompt-based inference.
    It evaluates the logits for the tokens ' positive' and
    ' negative', then returns the label with the higher score.
    """

    prompt = f"""
    Question: Is the following review positive or negative about the movie?
    Review: {review}
    Answer:
    """

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    final_logits = model(input_ids).logits[0, -1]

    # Compare token probabilities
    if final_logits[6785] > final_logits[8225]:
        print("Positive")
    else:
        print("Negative")
```

### How This Demonstrates Zero-Shot Generalization

* The model is not explicitly trained for this exact sentiment classification flow.
* Instead, it understands the prompt and predicts the most likely answer based on previously learned language patterns.
* The logits of the tokens " positive" and " negative" are compared, and the higher score determines the predicted sentiment.

This showcases how transformer models can generalize to new tasks using prompting alone, without additional task-specific training.

