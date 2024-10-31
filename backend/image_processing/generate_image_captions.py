# image_processing/generate_image_captions.py
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os
import psycopg2
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

def generate_captions(image_folder, model_name="Salesforce/blip-image-captioning-base"):
    """
    Generates captions for all images in the specified folder.
    
    :param image_folder: Directory containing images.
    :param model_name: Pretrained model name.
    :return: Dictionary mapping image paths to captions.
    """
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    
    image_files = sorted([
        f for f in os.listdir(image_folder) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    ])
    
    captions = {}
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        try:
            image = Image.open(image_path).convert('RGB')
            inputs = processor(image, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)
            captions[image_file] = caption
            print(f"Captioned {image_file}: {caption}")
        except Exception as e:
            print(f"Error captioning {image_file}: {e}")
    
    return captions

def store_image_captions(captions, db_config):
    """
    Stores image captions into the 'image_descriptions' table.
    
    :param captions: Dictionary mapping image filenames to captions.
    :param db_config: Database connection parameters.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO image_descriptions (document_id, page_number, image_path, caption, embedding)
            VALUES %s
        """
        # Assuming image filenames contain page numbers, e.g., 'page1_img1.png'
        data_to_insert = []
        for image_file, caption in captions.items():
            # Extract page number from filename
            parts = image_file.split('_')
            if len(parts) >= 2 and parts[0].startswith('page') and parts[1].startswith('img'):
                page_number = int(parts[0][4:])  # Extract number after 'page'
            else:
                page_number = 0  # Default or handle differently
            
            document_id = 'physics_notes'  # Modify if handling multiple documents
            image_path = os.path.join('../data/extracted_images/', image_file)
            
            # Generate embedding for the caption
            # Initialize the embedding model here or pass embeddings as a parameter
            # For simplicity, we'll generate embeddings here
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = embedding_model.encode(caption).tolist()
            
            data_to_insert.append((document_id, page_number, image_path, caption, embedding))
        
        execute_values(cursor, insert_query, data_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Stored {len(data_to_insert)} image captions into PostgreSQL.")
    except Exception as e:
        print(f"Error storing image captions: {e}")

if __name__ == "__main__":
    image_folder = '../data/extracted_images/'
    db_config = get_db_config()
    captions = generate_captions(image_folder)
    store_image_captions(captions, db_config)

