from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
from groq import Groq
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def create_vector_store(text):
    """
    Takes extracted document text
    Splits into chunks and stores as embeddings in FAISS
    Also creates BM25 index for keyword search
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Create BM25 index from same chunks
    tokenized_chunks = [chunk.lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)

    return vector_store, bm25, chunks


def hybrid_search(vector_store, bm25, chunks, question, k=5):
    """
    Combines FAISS semantic search and BM25 keyword search
    Returns top k most relevant chunks
    """
    # Semantic search using FAISS
    semantic_results = vector_store.similarity_search(question, k=k)
    semantic_chunks = [doc.page_content for doc in semantic_results]

    # Keyword search using BM25
    tokenized_question = question.lower().split()
    bm25_scores = bm25.get_scores(tokenized_question)
    top_bm25_indices = np.argsort(bm25_scores)[::-1][:k]
    bm25_chunks = [chunks[i] for i in top_bm25_indices]

    # Combine both results and remove duplicates
    combined = semantic_chunks + bm25_chunks
    seen = set()
    unique_chunks = []
    for chunk in combined:
        if chunk not in seen:
            seen.add(chunk)
            unique_chunks.append(chunk)

    # Return top k unique chunks
    return unique_chunks[:k]


def ask_question(vector_store_data, question, chat_history=[]):
    """
    Takes vector store data, user question and chat history
    Returns answer based on document content only
    Uses hybrid search for better retrieval quality
    """
    vector_store, bm25, chunks = vector_store_data

    # Get relevant chunks using hybrid search
    relevant_chunks = hybrid_search(
        vector_store, bm25, chunks, question, k=5
    )
    context = "\n".join(relevant_chunks)

    # Build messages with chat history
    messages = [
        {
            "role": "system",
            "content": """You are a legal document assistant.
            Answer questions based ONLY on the document content provided.
            If the answer is not in the document, say 
            'I could not find that in the document.'
            Keep answers simple and clear."""
        }
    ]

    for human, assistant in chat_history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})

    messages.append({
        "role": "user",
        "content": f"""Based on this document content:
{context}

Answer this question: {question}"""
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from core.extractor import extract_text

    text = extract_text("test.pdf")
    print("Creating vector store with hybrid search...")
    vs_data = create_vector_store(text)
    print("Done.")

    answer = ask_question(vs_data, "What is the rent amount?")
    print("Answer:", answer)