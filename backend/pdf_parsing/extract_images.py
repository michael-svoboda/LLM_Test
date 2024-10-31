# pdf_parsing/extract_images.py
import fitz  # PyMuPDF
import os

def extract_images(pdf_path, output_folder):
    """
    Extracts images from a PDF file and saves them to the specified folder.
    
    :param pdf_path: Path to the PDF file.
    :param output_folder: Directory where images will be saved.
    :return: List of paths to the extracted images.
    """
    try:
        pdf = fitz.open(pdf_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        image_list = []
        for page_number in range(len(pdf)):
            page = pdf[page_number]
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_path = os.path.join(
                    output_folder, f"page{page_number+1}_img{img_index+1}.{image_ext}"
                )
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                image_list.append(image_path)
        return image_list
    except Exception as e:
        print(f"Error extracting images from {pdf_path}: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    pdf_directory = '../data/'
    pdf_file = 'physics_notes.pdf'
    pdf_path = os.path.join(pdf_directory, pdf_file)
    
    images_output_folder = '../data/extracted_images/'
    images = extract_images(pdf_path, images_output_folder)
    
    print(f"Extracted {len(images)} images. Saved to {images_output_folder}")

