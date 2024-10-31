# image_processing/generate_image_embeddings.py
from sentence_transformers import SentenceTransformer
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()

def get_db_config():
    return {
        'dbname': os.getenv('DB_NAME', 'rag_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'your_password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

def load_captions(db_config):
    """
    Retrieves image captions from the 'image_descriptions' table.
    
    :param db_config: Database connection parameters.
    :return: List of tuples containing (id, caption).
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query_sql = """
            SELECT id, caption
            FROM image_descriptions
        """
        cursor.execute(query_sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error loading captions: {e}")
        return []

def generate_embeddings(captions, model_name='all-MiniLM-L6-v2'):
    """
    Generates embeddings for each caption.
    
    :param captions: List of captions.
    :param model_name: Name of the SentenceTransformer model.
    :return: List of embeddings.
    """
    model = SentenceTransformer(model_name)
    embeddings = [model.encode(caption) for _, caption in captions]
    return embeddings

def update_embeddings(captions, embeddings, db_config):
    """
    Updates the 'image_descriptions' table with the generated embeddings.
    
    :param captions: List of tuples containing (id, caption).
    :param embeddings: List of embeddings.
    :param db_config: Database connection parameters.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        update_query = """
            UPDATE image_descriptions
            SET embedding = data.embedding
            FROM (VALUES %s) AS data(id, embedding)
            WHERE image_descriptions.id = data.id
        """
        data_to_update = [
            (id_, emb.tolist()) for (id_, _), emb in zip(captions, embeddings)
        ]
        execute_values(cursor, update_query, data_to_update)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Updated {len(data_to_update)} image embeddings in PostgreSQL.")
    except Exception as e:
        print(f"Error updating embeddings: {e}")

if __name__ == "__main__":
    db_config = get_db_config()
    captions = load_captions(db_config)
    if captions:
        embeddings = generate_embeddings(captions)
        update_embeddings(captions, embeddings, db_config)
    else:
        print("No captions found to generate embeddings.")

