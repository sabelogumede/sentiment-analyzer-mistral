### Sentiment Analyzer using Mistral via Ollama
This README provides a comprehensive overview of the Sentiment Analyzer project, including setup instructions, features, architecture, and more. It is designed to be user-friendly and informative for anyone looking to understand or contribute to the project.


```markdown
# 🎭 Sentiment Analyzer using Mistral via Ollama

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.48.0-orange)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral-9cf)](https://ollama.com)

A **local, private, and explainable** sentiment analyzer that runs 100% on your machine — no internet, no data leaks.

Built with:
- 🔤 **FastAPI** – Backend API
- 🎨 **Streamlit** – Frontend UI
- 🧠 **Mistral via Ollama** – Local LLM for classification
- 💬 **Explainable AI** – Shows *why* a sentiment was assigned

Perfect for analyzing customer feedback, social media, emails, and more — all offline and secure.

---

## 🚀 Quick Start

### 1. Prerequisites

- [Python 3.9 or higher](https://www.python.org/downloads/)
- [Ollama](https://ollama.com/download) (to run Mistral locally)
- [Git](https://git-scm.com/downloads) (optional)

> ✅ Works on **Windows, macOS, and Linux**

---

### 2. Clone and Setup

```bash
# Clone the repo
git clone https://github.com/your-username/sentiment-analyzer-mistral.git
cd sentiment-analyzer-mistral

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Download the Mistral Model

```bash
# Start Ollama in the background
ollama serve
```

In another terminal:
```bash
ollama pull mistral
```

> 🧠 Downloads the Mistral model (~4.1GB). Only needed once.

---

### 4. Run the App

Open **two terminal windows**:

#### Terminal 1: Start FastAPI Backend
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2: Start Streamlit Frontend
```bash
streamlit run frontend/app.py
```

🌐 Open the app at: [http://localhost:8501](http://localhost:8501)

---

## 🖼️ Screenshot

![Sentiment Analyzer Screenshot](screenshots/screenshot.png)

> 💡 *Replace with your own screenshot! Save it in a `screenshots/` folder.*

---

## 🧱 Architecture

```
[User] 
   ↓
[Streamlit UI] → HTTP POST → [FastAPI Backend]
                                 ↓
                          [Ollama + Mistral]
                                 ↓
                      ← Sentiment + Explanation
```

- **Frontend**: `frontend/app.py` – Streamlit interface with live feedback
- **Backend**: `backend/main.py` – FastAPI with `/analyze` and `/explain` endpoints
- **Model**: Runs locally via Ollama (`mistral`)
- **Communication**: JSON over `localhost`

🔐 **No data leaves your machine. 100% private.**

---

## 🛠️ Features

- ✅ Classify sentiment as **Positive**, **Negative**, or **Neutral**
- ✅ **Explain why** the sentiment was assigned (e.g., "Uses words like 'love' and 'perfect'")
- ✅ Live **character count**
- ✅ Warning for **non-text input** (e.g., numbers)
- ✅ Input validation & error handling
- ✅ Color-coded results (🟢/🔴/🟡)
- ✅ Clear input button
- ✅ Responsive and intuitive UI

---

## 📂 Project Structure

```
sentiment-analyzer-mistral/
│
├── .gitignore               # Ignores venv, cache, IDE files
├── README.md                # This file
├── requirements.txt         # Python dependencies
│
├── backend/
│   └── main.py              # FastAPI backend with analysis + explanation
│
├── frontend/
│   └── app.py               # Streamlit frontend with explanation display
│
├── screenshots/             # (Optional) Add your app screenshots
│   └── screenshot.png
│
└── venv/                    # (Ignored) Virtual environment
```

---

## 📄 License

MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.

---

## 📌 Tips for Users

- ⏳ **Analysis takes 5–60 seconds** — be patient! The model runs locally.
- 📝 Best results with **natural language** (e.g., sentences with emotion).
- ⚠️ Inputs with no letters (e.g., `123 456`) are flagged as low-confidence.
- 🔍 The **"Why?"** section explains the reasoning behind the classification.
- 🗑️ Use the **"Clear Input & Result"** button to start over.

---

## 🚧 Future Improvements

- 📎 Support file uploads (TXT, CSV)
- 💾 Export results as `.txt` or `.json`
- 🔤 Highlight key sentiment words in input
- 📊 Confidence score (e.g., "High", "Medium", "Low")
- 🐳 Docker support for one-click setup
- 🌐 Multi-language sentiment analysis

---

## 🙌 Made with ❤️

By Sabelo Gumede – for **private, powerful, and explainable AI**.

Have ideas or feedback? Open an issue or PR!

Keep building the future — locally. 🚀
```