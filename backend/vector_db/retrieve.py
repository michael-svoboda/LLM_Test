# vector_db/retrieve.py
from sentence_transformers import SentenceTransformer
import psycopg2
import os
from dotenv import load_dotenv
import numpy as np

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

def get_top_k_embeddings(query, k=5, model_name='all-MiniLM-L6-v2'):
    """
    Retrieves the top k most similar text chunks to the query.
    
    :param query: User input query.
    :param k: Number of top results to retrieve.
    :param model_name: Name of the SentenceTransformer model.
    :return: List of tuples containing (id, content, distance).
    """
    model = SentenceTransformer(model_name)
    query_emb = model.encode(query)
    
    db_config = get_db_config()
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        # PostgreSQL uses <-> for distance; assuming Euclidean distance
        query_sql = """
            SELECT id, content, embedding <-> %s AS distance
            FROM text_chunks
            ORDER BY distance
            LIMIT %s
        """
        cursor.execute(query_sql, (query_emb.tolist(), k))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error retrieving embeddings: {e}")
        return []

if __name__ == "__main__":
    user_query = "Explain the data processing pipeline diagram."
    top_k = 3
    results = get_top_k_embeddings(user_query, k=top_k)
    
    print(f"Top {top_k} results for query: '{user_query}'\n")
    for res in results:
        print(f"ID: {res[0]}, Distance: {res[2]:.4f}\nContent: {res[1]}\n")

