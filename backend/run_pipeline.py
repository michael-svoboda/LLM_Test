# run_pipeline.py
import subprocess
import os

def run_script(script_path):
    """
    Runs a Python script using subprocess.
    
    :param script_path: Path to the Python script.
    """
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

def main():
    # Define script paths
    pdf_parsing_dir = 'pdf_parsing'
    vector_db_dir = 'vector_db'
    image_processing_dir = 'image_processing'
    scripts_dir = 'scripts'

    # Step 1: Extract text
    print("Extracting text from PDF...")
    extract_text_script = os.path.join(pdf_parsing_dir, 'extract_text.py')
    run_script(extract_text_script)

    # Step 2: Extract images
    print("Extracting images from PDF...")
    extract_images_script = os.path.join(pdf_parsing_dir, 'extract_images.py')
    run_script(extract_images_script)

    # Step 3: Process text
    print("Processing extracted text...")
    process_text_script = os.path.join(pdf_parsing_dir, 'process_text.py')
    run_script(process_text_script)

    # Step 4: Chunk text
    print("Chunking processed text...")
    chunk_text_script = os.path.join(pdf_parsing_dir, 'chunk_text.py')
    run_script(chunk_text_script)

    # Step 5: Generate and store text embeddings
    print("Generating and storing text embeddings...")
    store_embeddings_script = os.path.join(vector_db_dir, 'store_embeddings.py')
    run_script(store_embeddings_script)

    # Step 6: Generate and store image captions
    print("Generating and storing image captions...")
    generate_image_captions_script = os.path.join(image_processing_dir, 'generate_image_captions.py')
    run_script(generate_image_captions_script)

    # Optional: Generate and store image embeddings separately
    # print("Generating and storing image embeddings...")
    # generate_image_embeddings_script = os.path.join(image_processing_dir, 'generate_image_embeddings.py')
    # run_script(generate_image_embeddings_script)

    # Step 7: Retrieve (for testing)
    print("Retrieving relevant text chunks...")
    retrieve_script = os.path.join(vector_db_dir, 'retrieve.py')
    run_script(retrieve_script)

if __name__ == "__main__":
    main()

