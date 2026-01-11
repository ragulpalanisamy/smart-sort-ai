# 🧠 Smart Sort AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![AI](https://img.shields.io/badge/AI-Sentence--Transformers-orange?style=for-the-badge)](https://www.sbert.net/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ragulpalanisamy/smart-sort-ai?style=for-the-badge)](https://github.com/ragulpalanisamy/smart-sort-ai)

> **Stop organizing files by extension. Start organizing them by _meaning_.**

**Smart Sort AI** is a professional-grade, local-first automation tool that uses Neural Networks to understand your file's purpose and sort it into logical categories.

---

## ✨ Why Smart Sort AI?

Traditional file sorters are "dumb"—they put all `.pdf` files in one folder. **Smart Sort AI** actually reads the filename and understands context:

- `invoice_2024_jan.pdf` → **📂 Finance**
- `project_proposal_draft.docx` → **📂 Work**
- `hawaii_vacation_001.jpg` → **📂 Personal**
- `main.py` → **📂 Tech**

### 🛡️ Privacy First

No APIs. No Clouds. Your data never leaves your machine. Everything runs locally using `sentence-transformers`.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-sort-ai.git
cd smart-sort-ai

# Create a virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install professional dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

Organize your Downloads folder with a simple command:

```bash
python3 main.py ~/Downloads
```

### 3. Dry Run (Safety First)

Check where files _would_ go without actually moving them:

```bash
python3 main.py ~/Downloads --dry-run
```

---

## 🛠 Features

- [x] **Contextual Embedding**: Uses `all-MiniLM-L6-v2` for high-speed, local similarity matching.
- [x] **Beautiful CLI**: Powered by `Rich` for professional terminal tables and progress bars.
- [x] **Smart Cleaning**: Automatically strips extensions and cleans separators (dots, underscores) for better AI understanding.
- [x] **Safety Thresholds**: Only moves files when the AI is confident (customizable via `--threshold`).
- [x] **Dry Run Mode**: Preview changes before committing.

---

## 📖 How It Works

1. **Preprocessing**: The script cleans the filename (e.g., `tax_return_2023.pdf` becomes `tax return 2023`).
2. **Vectorization**: It converts the filename into a mathematical vector (embedding) using a Transformer model.
3. **Similarity Search**: It compares that vector against pre-defined category descriptions using **Cosine Similarity**.
4. **Execution**: The file is moved to the highest-scoring category if it exceeds the confidence threshold.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

_Built with ❤️ for a cleaner desktop._
