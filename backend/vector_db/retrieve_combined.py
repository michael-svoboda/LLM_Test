# vector_db/retrieve_combined.py
from sentence_transformers import SentenceTransformer
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    return {
        'dbname': os.getenv('DB_NAME', 'rag_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'your_password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

def retrieve_text_chunks(query, k=5, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    query_emb = model.encode(query)
    
    db_config = get_db_config()
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query_sql = """
            SELECT id, content, embedding <-> %s AS distance
            FROM text_chunks
            ORDER BY distance
            LIMIT %s
        """
        cursor.execute(query_sql, (query_emb.tolist(), k))
        text_results = cursor.fetchall()
        cursor.close()
        conn.close()
        return text_results
    except Exception as e:
        print(f"Error retrieving text embeddings: {e}")
        return []

def retrieve_image_captions(query, k=5, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    query_emb = model.encode(query)
    
    db_config = get_db_config()
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query_sql = """
            SELECT id, caption, embedding <-> %s AS distance
            FROM image_descriptions
            ORDER BY distance
            LIMIT %s
        """
        cursor.execute(query_sql, (query_emb.tolist(), k))
        image_results = cursor.fetchall()
        cursor.close()
        conn.close()
        return image_results
    except Exception as e:
        print(f"Error retrieving image embeddings: {e}")
        return []

if __name__ == "__main__":
    user_query = "Describe the data flow in the system."
    top_k = 3
    
    text_results = retrieve_text_chunks(user_query, k=top_k)
    image_results = retrieve_image_captions(user_query, k=top_k)
    
    print(f"Top {top_k} Text Chunks:\n")
    for res in text_results:
        print(f"ID: {res[0]}, Distance: {res[2]:.4f}\nContent: {res[1]}\n")
    
    print(f"Top {top_k} Image Captions:\n")
    for res in image_results:
        print(f"ID: {res[0]}, Distance: {res[2]:.4f}\nCaption: {res[1]}\n")

