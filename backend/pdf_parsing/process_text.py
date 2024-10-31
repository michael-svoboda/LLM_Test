# pdf_parsing/process_text.py
import re
import os

def clean_text(text):
    """
    Cleans and normalizes the extracted text.
    
    :param text: Raw extracted text.
    :return: Cleaned text.
    """
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove unwanted characters (optional)
    # text = re.sub(r'[^A-Za-z0-9 .,;!?()\[\]\'\"-]', '', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    return text

def save_cleaned_text(input_path, output_path):
    """
    Reads raw text from input_path, cleans it, and writes to output_path.
    
    :param input_path: Path to the raw text file.
    :param output_path: Path to save the cleaned text.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        cleaned = clean_text(raw_text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"Cleaned text saved to {output_path}")
    except Exception as e:
        print(f"Error processing text: {e}")

if __name__ == "__main__":
    # Example usage
    data_directory = '../data/'
    raw_text_file = 'extracted_text.txt'
    cleaned_text_file = 'cleaned_text.txt'
    
    input_path = os.path.join(data_directory, raw_text_file)
    output_path = os.path.join(data_directory, cleaned_text_file)
    
    save_cleaned_text(input_path, output_path)

