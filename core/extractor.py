import pdfplumber
import easyocr
import os

def extract_from_pdf(file_path):
    """Extract text from a PDF file"""
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n--- Page {i+1} ---\n"
                full_text += text
            else:
                full_text += f"\n--- Page {i+1}: No text found ---\n"
    return full_text


def extract_from_image(file_path):
    """Extract text from an image using OCR"""
    reader = easyocr.Reader(['en'])
    results = reader.readtext(file_path)
    full_text = ""
    for (bbox, text, prob) in results:
        full_text += text + " "
    return full_text.strip()


def extract_text(file_path):
    """
    Main function — detects file type automatically
    Handles both PDF and images
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_from_pdf(file_path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        return extract_from_image(file_path)
    else:
        return "Unsupported file type."


if __name__ == "__main__":
    result = extract_text("test.pdf")
    print(result)