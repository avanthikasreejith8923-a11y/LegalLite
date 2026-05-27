from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def create_vector_store(text):
    """
    Takes extracted document text
    Splits into chunks and stores as embeddings in FAISS
    """
    # Split document into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    # Convert chunks to embeddings and store in FAISS
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    return vector_store


def ask_question(vector_store, question, chat_history=[]):
    """
    Takes vector store, user question and chat history
    Returns answer based on document content only
    """
    # Find relevant chunks from document
    relevant_chunks = vector_store.similarity_search(question, k=3)
    context = "\n".join([chunk.page_content for chunk in relevant_chunks])

    # Build messages with chat history
    messages = [
        {
            "role": "system",
            "content": """You are a legal document assistant. 
            Answer questions based ONLY on the document content provided.
            If the answer is not in the document, say 'I could not find that in the document.'
            Keep answers simple and clear."""
        }
    ]

    # Add chat history
    for human, assistant in chat_history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})

    # Add current question with context
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
    print("Creating vector store...")
    vs = create_vector_store(text)
    print("Vector store created.")
    
    answer = ask_question(vs, "What is the rent amount?")
    print("Answer:", answer)