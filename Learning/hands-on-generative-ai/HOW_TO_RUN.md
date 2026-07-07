# 🚀 How to Run Python Files in This Workspace

This guide explains how to properly run the Python scripts (such as `PreparingTheData.py` in Chapter 3) and Jupyter notebooks in this workspace using the local virtual environment (`.venv`).

---

## 🛠️ Option 1: Direct Execution (Recommended)
You can run any Python file directly using the virtual environment's Python interpreter without needing to manually activate the environment first. This is the cleanest and most robust method.

Run this command from the `Learning/hands-on-generative-ai/` directory:

```bash
# General format:
.venv/bin/python <path_to_file>

# Example: Run the Chapter 3 MNIST data preparation script:
.venv/bin/python 03_compressing_and_representing_information/PreparingTheData.py
```

---

## 🔄 Option 2: Active Environment Execution
If you prefer to work interactively or run multiple commands, you can activate the virtual environment in your terminal session.

### 1. Activate the Virtual Environment
From the `Learning/hands-on-generative-ai/` directory, run:
```bash
source .venv/bin/activate
```
*(Your terminal prompt should now be prefixed with `(.venv)`)*

### 2. Run the Script
Now you can run the files using the standard `python` or `python3` command:
```bash
python 03_compressing_and_representing_information/PreparingTheData.py
```

### 3. Deactivate when Finished
To exit the virtual environment and return to your global system Python environment, simply run:
```bash
deactivate
```

---

## 📓 Option 3: Running Jupyter Notebooks
To open and run the `.ipynb` notebooks using the packages installed in the virtual environment:

1. Navigate to the `Learning/hands-on-generative-ai/` directory.
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Launch Jupyter Lab:
   ```bash
   jupyter lab
   ```
4. This will open Jupyter in your browser. Select the notebook you wish to run and ensure the kernel is set to the `.venv` Python interpreter.

---

## 🔍 Troubleshooting
If you encounter a `ModuleNotFoundError` (e.g., `No module named 'datasets'`):
* Make sure you are executing the file using `.venv/bin/python` or that your terminal says `(.venv)` at the beginning of the prompt.
* If a package is missing, you can install it using pip inside the virtual environment:
  ```bash
  .venv/bin/pip install <package_name>
  ```
