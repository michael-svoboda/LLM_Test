# pdf_parsing/chunk_text.py
from transformers import AutoTokenizer
import os

def chunk_text(text, max_tokens=500, overlap=50, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    """
    Splits text into chunks suitable for LLM processing.
    
    :param text: The cleaned text to be chunked.
    :param max_tokens: Maximum number of tokens per chunk.
    :param overlap: Number of overlapping tokens between chunks.
    :param model_name: Name of the tokenizer model.
    :return: List of text chunks.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
        start += max_tokens - overlap
    return chunks

def save_chunks(chunks, output_dir):
    """
    Saves each text chunk to a separate file in the specified directory.
    
    :param chunks: List of text chunks.
    :param output_dir: Directory to save the chunk files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, chunk in enumerate(chunks, start=1):
        chunk_filename = f'chunk_{i}.txt'
        chunk_path = os.path.join(output_dir, chunk_filename)
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
    
    print(f"Saved {len(chunks)} text chunks to {output_dir}")

if __name__ == "__main__":
    # Example usage
    data_directory = '../data/'
    cleaned_text_file = 'cleaned_text.txt'
    chunks_output_dir = '../data/chunks/'
    
    input_path = os.path.join(data_directory, cleaned_text_file)
    output_dir = chunks_output_dir
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            cleaned_text = f.read()
        
        chunks = chunk_text(cleaned_text)
        save_chunks(chunks, output_dir)
    except Exception as e:
        print(f"Error chunking text: {e}")

