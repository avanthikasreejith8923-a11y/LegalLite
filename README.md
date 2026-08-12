# LegalLite

### AI that reads the fine print so you don't have to.

Most people sign legal documents without truly understanding what they are agreeing to. A single missed clause can cost thousands. LegalLite changes that — upload any contract, agreement or notice and get a clear, honest breakdown of exactly what it means, what is risky, and what to watch out for. No lawyers. No jargon. Just clarity.

---

## Live Demo

Try it live at https://legallite.streamlit.app/

---

## What LegalLite Can Do

**Understand any document**
Upload a PDF or a photo of any legal document — rental agreements, employment letters, NDAs, loan documents, insurance papers. LegalLite reads it all, including tables and structured data buried inside.

**Speak your language**
Legal clarity should not be limited by language. Get your document explained in Malayalam, Hindi, Tamil, Telugu, Kannada, Bengali, French or Arabic — instantly.

**Catch what you might miss**
Hidden penalties. Auto-renewal traps. One-sided conditions. Vague payment terms. LegalLite flags the risks buried in the fine print before you sign anything.

**Ask anything**
Have a question about a specific clause? Just ask. The AI answers directly from your document using a hybrid RAG pipeline — not from guesswork, not from hallucination.

**Listen instead of read**
Not in the mood to read? Let LegalLite read the summary to you in your language with AI voice output.

---

## How It Works

```
User uploads PDF or image
        |
Text and table extraction using pdfplumber or EasyOCR
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
        |--- Semantic search using FAISS
        |--- Keyword search using BM25
        |
Hybrid retrieval combines both results
        |
RAG Chatbot answers questions from document only
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq API, Llama 3.3 70B |
| RAG Pipeline | LangChain, FAISS, BM25 Hybrid Search |
| Embeddings | sentence-transformers, all-MiniLM-L6-v2 |
| PDF Extraction | pdfplumber with table extraction |
| Image OCR | EasyOCR with confidence filtering |
| Translation | deep-translator |
| Voice Output | gTTS |
| Language | Python 3.11 |

---

## Project Structure

```
legallite/
├── app.py                  Streamlit UI
├── core/
│   ├── extractor.py        PDF, table and image text extraction
│   ├── summarizer.py       LLM summarization and risk detection
│   ├── rag.py              Hybrid RAG pipeline and chatbot
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

---

## Concepts Used

- Retrieval Augmented Generation
- Hybrid search combining semantic and keyword retrieval
- Vector embeddings and semantic search
- BM25 keyword ranking
- Hierarchical document parsing with table extraction
- Large Language Model integration
- Optical Character Recognition with confidence filtering
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
