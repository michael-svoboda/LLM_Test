# vector_db/store_embeddings.py
from sentence_transformers import SentenceTransformer
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_db_config():
    """
    Retrieves database configuration from environment variables.
    
    :return: Dictionary containing database connection parameters.
    """
    return {
        'dbname': os.getenv('DB_NAME', 'rag_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'your_password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

def generate_embeddings(model_name='all-MiniLM-L6-v2'):
    """
    Generates embeddings for all text chunks in the 'chunks/' directory.
    
    :param model_name: Name of the SentenceTransformer model.
    :return: List of tuples containing (document_id, page_number, content, embedding).
    """
    model = SentenceTransformer(model_name)
    chunks_dir = '../data/chunks/'
    chunk_files = sorted([f for f in os.listdir(chunks_dir) if f.endswith('.txt')])
    embeddings = []
    for file in chunk_files:
        with open(os.path.join(chunks_dir, file), 'r', encoding='utf-8') as f:
            text = f.read()
            emb = model.encode(text)
            # Extract chunk number from filename, e.g., 'chunk_1.txt'
            chunk_number = int(file.split('_')[1].split('.')[0])
            document_id = 'physics_notes'  # Modify if handling multiple documents
            embeddings.append((document_id, chunk_number, text, emb.tolist()))
    return embeddings

def store_embeddings(embeddings, db_config):
    """
    Stores embeddings into the 'text_chunks' table in PostgreSQL.
    
    :param embeddings: List of tuples containing embedding data.
    :param db_config: Database connection parameters.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO text_chunks (document_id, page_number, content, embedding)
            VALUES %s
        """
        # Prepare data for insertion
        data_to_insert = [
            (doc_id, page_num, content, emb)
            for doc_id, page_num, content, emb in embeddings
        ]
        # Use execute_values for efficient bulk insert
        execute_values(cursor, insert_query, data_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Stored {len(embeddings)} text embeddings into PostgreSQL.")
    except Exception as e:
        print(f"Error storing embeddings: {e}")

if __name__ == "__main__":
    db_config = get_db_config()
    embeddings = generate_embeddings()
    store_embeddings(embeddings, db_config)

