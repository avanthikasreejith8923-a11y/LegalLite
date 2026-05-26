import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_document(text):
    """
    Takes extracted text from a legal document
    Returns a plain English summary
    """
    prompt = f"""
    You are a legal document assistant. 
    Read the following legal document and explain it in very simple, 
    plain English that anyone can understand.
    
    Structure your response as:
    1. What is this document about?
    2. Key points to know
    3. Important dates or numbers mentioned
    4. What you are agreeing to
    
    Document:
    {text}
    """
    
    response = model.generate_content(prompt)
    return response.text


def detect_risks(text):
    """
    Takes extracted text
    Returns list of risky clauses found
    """
    prompt = f"""
    You are a legal risk detector.
    Read this legal document and find any risky or unfair clauses.
    
    Look for:
    - Hidden penalties
    - Auto renewal clauses
    - Unfair termination conditions
    - Vague payment terms
    - One sided conditions
    
    List each risk clearly and simply.
    
    Document:
    {text}
    """
    
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Test it with our test PDF
    from core.extractor import extract_text
    
    text = extract_text("test.pdf")
    print("=== SUMMARY ===")
    print(summarize_document(text))
    print("\n=== RISKS ===")
    print(detect_risks(text))