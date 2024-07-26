import os
from pdf2image import convert_from_path
from easyocr import Reader
import pandas as pd

def pdf_to_images(pdf_path, image_dir):
    images = convert_from_path(pdf_path, 500)  # Ajuste a resolução conforme necessário
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, image in enumerate(images):
        image_name = f"{pdf_name}_page_{i + 1}.jpg"
        image_path = os.path.join(image_dir, image_name)
        image.save(image_path, 'JPEG')

def ocr_on_images(image_dir):
    reader = Reader(['pt'])  # Use o idioma desejado
    list_data = []
    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpg"):
            image_path = os.path.join(image_dir, image_file)
            results = reader.readtext(image_path)
            list_data +=results 
            print(f"OCR Results for {image_file}: Done!")
    data=pd.DataFrame(list_data, columns=['bbox', 'text', 'prob'])
    data.to_csv(f'data_{image_file}.csv', index=False)

    # Apagar imagens após OCR
    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpg"):
            image_path = os.path.join(image_dir, image_file)
            os.remove(image_path)

if __name__ == "__main__":
    pdf_directory = "images/entrada"     # caminho para o diretório contendo os arquivos PDF
    image_directory = "images/saida"    # diretório para salvar as imagens temporárias geradas a partir dos PDFs

    os.makedirs(image_directory, exist_ok=True)

    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, pdf_file)

            pdf_to_images(pdf_path, image_directory)
            ocr_on_images(image_directory)
