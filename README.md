# LegalLite

AI that reads the fine print so you don't have to.

Legal documents are long, complex and full of clauses that are easy to miss. LegalLite changes that — upload any contract, agreement or notice and instantly get a clear breakdown of what it means, what is risky, and what to watch out for.

---

## Live Demo

legallite.streamlit.app

---

## Features

- Document Upload — Upload any PDF, JPG or PNG file including rental agreements, employment letters, NDAs, loan documents and insurance papers.
- Plain English Summary — Reads the entire document and explains it in simple language anyone can understand. No legal jargon.
- Risk Detection — Automatically identifies hidden penalties, auto-renewal clauses, unfair termination conditions, vague payment terms and one-sided conditions.
- Multilingual Translation — Explains your document in Malayalam, Hindi, Tamil, Telugu, Kannada, Bengali, French and Arabic.
- Voice Output — Reads the summary aloud in your chosen language using AI text-to-speech.
- AI Document Chatbot — Ask any question about your document and get answers grounded in the actual document content. Built on a RAG pipeline using FAISS and sentence-transformers.

---

## How It Works

```
User uploads PDF or image
        |
Text extraction using pdfplumber or EasyOCR
        |
LLM processing using Groq and Llama 3
        |
        |--- Plain English Summary
        |--- Risk Flag Detection
        |--- Multilingual Translation
        |--- Voice Output
        |
Document chunking and embeddings using sentence-transformers
        |
Vector storage using FAISS
        |
RAG Chatbot answers questions from document only
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq API, Llama 3.3 70B |
| RAG Pipeline | LangChain, FAISS |
| Embeddings | sentence-transformers, all-MiniLM-L6-v2 |
| PDF Extraction | pdfplumber |
| Image OCR | EasyOCR |
| Translation | deep-translator |
| Voice Output | gTTS |
| Language | Python 3.11 |

---

## Project Structure

```
legallite/
├── app.py                  Streamlit UI
├── core/
│   ├── extractor.py        PDF and image text extraction
│   ├── summarizer.py       LLM summarization and risk detection
│   ├── rag.py              RAG pipeline and document chatbot
│   ├── translator.py       Multilingual translation
│   └── voice.py            Text to speech output
├── requirements.txt        All dependencies
├── .env                    API keys (not pushed to GitHub)
└── README.md
```

---

## Run Locally

Clone the repository

```
git clone https://github.com/avanthikasreejith8923-a11y/LegalLite.git
cd LegalLite
```

Create and activate virtual environment

```
python -m venv venv
source venv/Scripts/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Create a .env file and add your Groq API key

```
GROQ_API_KEY=your_key_here
```

Run the app

```
streamlit run app.py
```

Open your browser at http://localhost:8501

---

## Concepts Used

- Retrieval Augmented Generation
- Vector embeddings and semantic search
- Large Language Model integration
- Optical Character Recognition
- Natural Language Processing
- Prompt engineering
- Multilingual AI

---

## Disclaimer

This tool is for informational purposes only. It is not a substitute for professional legal advice.

---
## Author

Avanthika Sreejith

GitHub: avanthikasreejith8923-a11y










































