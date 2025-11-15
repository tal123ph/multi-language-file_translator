# 🌍 Multi-Language Translator (Streamlit + Lingo.dev)

This project is a **Streamlit web app** that translates text, SRT subtitles, TXT files, and PDFs into multiple languages using the Lingo.dev API. Users can upload a file, select a target language, and download the translated output in PDF, TXT, or SRT format.  

---

## Features

- Upload `.srt`, `.txt`, or `.pdf` files
- Translate into multiple languages
- Output as PDF, TXT, or SRT
- Async translation using Lingo.dev
- Handles large files with error handling
- Download translated files instantly

---

## Setup Instructions

1. Clone this repository:

```bash
git clone https://github.com/tal123ph/multi-language-translator.git
cd multi-language-translator

multi-language-translator/
│
├── .streamlit/        # Streamlit secrets folder
├── venv/              # Virtual environment
├── .ignoregit         # Ye galat naam hai, should be .gitignore
├── app.py             # Streamlit app
└── README.md          # Project description

