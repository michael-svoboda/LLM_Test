# pdf_parsing/extract_text.py
from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

if __name__ == "__main__":
    # Example usage
    pdf_directory = '../data/'  # Relative path to data directory
    pdf_file = 'physics_notes.pdf'
    pdf_path = os.path.join(pdf_directory, pdf_file)
    
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Save extracted text to a file
    output_path = os.path.join(pdf_directory, 'extracted_text.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    
    print(f"Text extraction complete. Saved to {output_path}")

