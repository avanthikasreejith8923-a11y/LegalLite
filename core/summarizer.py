import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_document(text):
    """
    Takes extracted text from a legal document
    Returns a plain English summary
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a legal document assistant who explains legal documents in very simple plain English that anyone can understand."
            },
            {
                "role": "user",
                "content": f"""Read the following legal document and explain it simply.
                
Structure your response as:
1. What is this document about?
2. Key points to know
3. Important dates or numbers mentioned
4. What you are agreeing to

Document:
{text}"""
            }
        ]
    )
    return response.choices[0].message.content


def detect_risks(text):
    """
    Takes extracted text
    Returns list of risky clauses found
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a legal risk detector who finds risky or unfair clauses in legal documents."
            },
            {
                "role": "user",
                "content": f"""Read this legal document and find any risky or unfair clauses.

Look for:
- Hidden penalties
- Auto renewal clauses
- Unfair termination conditions
- Vague payment terms
- One sided conditions

List each risk clearly and simply.

Document:
{text}"""
            }
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    from core.extractor import extract_text
    
    text = extract_text("test.pdf")
    print("=== SUMMARY ===")
    print(summarize_document(text))
    print("\n=== RISKS ===")
    print(detect_risks(text))