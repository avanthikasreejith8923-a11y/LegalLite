import pdfplumber
import easyocr
import os


def extract_tables_from_page(page):
    """
    Extracts tables from a PDF page and converts
    them into readable structured text
    """
    tables = page.extract_tables()
    table_text = ""

    for table_index, table in enumerate(tables):
        table_text += f"\n[TABLE {table_index + 1}]\n"

        # Get header row
        if not table or len(table) == 0:
            continue

        header = table[0]

        # Process each row
        for row_index, row in enumerate(table):
            if row_index == 0:
                # Header row
                clean_header = [
                    str(cell).strip() if cell else "N/A"
                    for cell in row
                ]
                table_text += " | ".join(clean_header) + "\n"
                table_text += "-" * 40 + "\n"
            else:
                # Data rows — combine header with value
                for col_index, cell in enumerate(row):
                    if col_index < len(header):
                        col_name = str(header[col_index]).strip() \
                            if header[col_index] else f"Column {col_index + 1}"
                        cell_value = str(cell).strip() if cell else "N/A"
                        table_text += f"{col_name}: {cell_value}\n"
                table_text += "\n"

        table_text += f"[END TABLE {table_index + 1}]\n"

    return table_text


def extract_from_pdf(file_path):
    """
    Extracts both text and tables from a PDF file.
    Tables are converted to structured readable format.
    Regular text and table text are combined.
    """
    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            full_text += f"\n--- Page {i + 1} ---\n"

            # Extract regular text
            text = page.extract_text()
            if text:
                full_text += text + "\n"
            else:
                full_text += "[No text found on this page]\n"

            # Extract tables separately
            table_text = extract_tables_from_page(page)
            if table_text.strip():
                full_text += "\n[STRUCTURED TABLE DATA]\n"
                full_text += table_text

    return full_text


def extract_from_image(file_path):
    """
    Extracts text from an image using EasyOCR.
    Handles multiple languages.
    """
    reader = easyocr.Reader(['en'])
    results = reader.readtext(file_path)

    full_text = ""
    for (bbox, text, prob) in results:
        # Only include text with confidence above 50%
        if prob > 0.5:
            full_text += text + " "

    return full_text.strip()


def extract_text(file_path):
    """
    Main function — detects file type automatically.
    Handles PDF, images and scanned documents.
    Returns combined text and table data.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_from_pdf(file_path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        return extract_from_image(file_path)
    else:
        return "Unsupported file type."


if __name__ == "__main__":
    # Create a test PDF with a table
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10,
             txt="This rental agreement is between landlord and tenant.",
             ln=True)
    pdf.cell(200, 10,
             txt="Tenant must pay rent before 5th of every month.",
             ln=True)
    pdf.output("test.pdf")

    result = extract_text("test.pdf")
    print(result)