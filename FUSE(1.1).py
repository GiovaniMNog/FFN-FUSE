#FUSE: Futsal Summary Extractor

import os
from pdf2image import convert_from_path
from PIL import Image
import easyocr
import pandas as pd

def pdf_to_images(pdf_path):
    """Converts PDF to a list of images."""
    images = convert_from_path(pdf_path)
    return images

def ocr_image(image, reader):
    """Performs OCR on a PIL image and returns the extracted text."""
    # Converte a imagem PIL para formato necessário pelo easyocr
    img_path = "temp_image.jpg"
    image.save(img_path)
    results = reader.readtext(
        img_path,                    
        detail=1                   
    )
    # Organiza os resultados em listas separadas
    bboxes = [result[0] for result in results]
    texts = [result[1] for result in results]
    probs = [result[2] for result in results]
    return bboxes, texts, probs

def process_ocr_results(bboxes, texts, probs):
    """
    Process OCR results into a structured DataFrame with specific columns.
    """
    data = {
        'coordenada 1 da bbox': [bbox[0] for bbox in bboxes],
        'coordenada 2': [bbox[1] for bbox in bboxes],
        'coordenada 3': [bbox[2] for bbox in bboxes],
        'coordenada 4': [bbox[3] for bbox in bboxes],
        'text': texts,
        'prob': probs
    }
    df = pd.DataFrame(data)
    return df

def save_text_to_csv(df, csv_path):
    """Saves the organized DataFrame to a CSV file."""
    df.to_csv(csv_path, index=False)

def concatenate_and_remove_csvs(base_filename, output_directory):
    """Concatenates all CSV files for a single document into one CSV file and removes the original CSVs."""
    csv_files = [os.path.join(output_directory, f) for f in os.listdir(output_directory) if f.startswith(base_filename) and f.endswith('.csv')]
    combined_df = pd.concat([pd.read_csv(f) for f in csv_files])
    concatenated_csv_path = os.path.join(output_directory, f"{base_filename}_combined.csv")
    combined_df.to_csv(concatenated_csv_path, index=False)
    print(f"Concatenated CSV saved to {concatenated_csv_path}")

    # Remove os arquivos CSV intermediários
    for csv_file in csv_files:
        os.remove(csv_file)
        print(f"Removed intermediate CSV file {csv_file}")

def process_pdfs_in_directory(input_directory, output_directory):
    """Processes all PDFs in a directory and saves CSVs to a specified directory."""
    reader = easyocr.Reader(['pt'])  # Inicializa o easyocr com suporte para português
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_directory, filename)
            print(f"Processing {pdf_path}...")

            images = pdf_to_images(pdf_path)
            base_filename = os.path.splitext(filename)[0]
            for i, image in enumerate(images):
                bboxes, texts, probs = ocr_image(image, reader)
                df = process_ocr_results(bboxes, texts, probs)
                csv_path = os.path.join(output_directory, f"{base_filename}_page_{i+1}.csv")
                save_text_to_csv(df, csv_path)
                print(f"Saved OCR text to {csv_path}")

            # Concatena os CSVs das páginas em um único CSV e remove os CSVs intermediários
            concatenate_and_remove_csvs(base_filename, output_directory)

# Define o diretório contendo os PDFs e o diretório de saída para os CSVs
input_directory = 'images/input'
output_directory = 'images/output'

# Cria o diretório de saída se ele não existir
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Processa os PDFs no diretório de entrada e salva os CSVs no diretório de saída
def __main__():
    process_pdfs_in_directory(input_directory, output_directory)

if __name__ == "__main__":
    __main__()

# Fim do arquivo FUSE.py