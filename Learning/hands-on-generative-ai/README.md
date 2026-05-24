# Hands-On Generative AI with Transformers and Diffusion Models

Welcome to your hands-on learning workspace for the O'Reilly book **"Hands-On Generative AI with Transformers and Diffusion Models"** by Omar Sanseviero, Pedro Cuenca, Apolinário Passos, and Jonathan Whitaker.

This repository is designed to keep your notes, code experiments, and exercises structured as you progress through each chapter.

---

## 📚 Book Resources
*   **Official GitHub Repository:** [genaibook/genaibook](https://github.com/genaibook/genaibook)
*   **Hugging Face Organization:** [genaibook on Hugging Face](https://huggingface.co/genaibook) (contains datasets, models, and spaces used throughout the book)
*   **Helper Python Library:** [genaibook on PyPI](https://pypi.org/project/genaibook/)

---

## 🛠️ Environment Setup

To run the notebooks locally, it is recommended to set up a virtual environment:

### 1. Create a Virtual Environment
```bash
# Navigate to this directory
cd Learning/hands-on-generative-ai

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install required dependencies
pip install -r requirements.txt
```

> [!TIP]
> Since generative AI models (especially for diffusion and fine-tuning) can be highly computationally intensive, you may want to run some of these notebooks in a GPU-accelerated environment such as **Google Colab** or **Kaggle Notebooks**. Use the links inside each chapter folder to launch them directly.

---

## 📖 Chapter Index

| Chapter | Title | Key Topics Covered | Workspace Link |
| :---: | :--- | :--- | :--- |
| **01** | **Introduction to Generative Media** | Generative vs. discriminative, history, pipeline setup | [Chapter 1](./01_introduction_to_generative_media/) |
| **02** | **Transformers** | Attention mechanism, encoder/decoder, GPT, BERT | [Chapter 2](./02_transformers/) |
| **03** | **Compressing and Representing Information** | Embeddings, autoencoders, vector search, semantic space | [Chapter 3](./03_compressing_and_representing_information/) |
| **04** | **Diffusion Models** | Forward/reverse diffusion, DDPM, noise prediction | [Chapter 4](./04_diffusion_models/) |
| **05** | **Stable Diffusion & Conditional Gen** | Latent diffusion, CLIP, classifier-free guidance, prompts | [Chapter 5](./05_stable_diffusion_and_conditional_generation/) |
| **06** | **Fine-Tuning Language Models** | SFT, LoRA, QLoRA, Reinforcement Learning (RLHF/DPO) | [Chapter 6](./06_fine_tuning_language_models/) |
| **07** | **Fine-Tuning Stable Diffusion** | DreamBooth, Textual Inversion, LoRA, ControlNet | [Chapter 7](./07_fine_tuning_stable_diffusion/) |
| **08** | **Creative Applications** | Outpainting, inpainting, image-to-image, pipeline hacks | [Chapter 8](./08_creative_applications_of_text_to_image_models/) |
| **09** | **Generating Audio** | Spectrograms, AudioLDM, text-to-speech (TTS), MusicGen | [Chapter 9](./09_generating_audio/) |

---

## 🚀 Getting Started
Launch Jupyter Lab or Notebook to begin:
```bash
jupyter lab
```
Navigate to the chapter you are currently studying and open its notebook to start coding!
