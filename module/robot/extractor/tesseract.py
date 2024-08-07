import pytesseract
import os
from pdf2image import convert_from_path, convert_from_bytes
from io import BytesIO
from PIL import Image


# TODO: Deixar configuravel para o usuario windows e remover caso esteja no linux
poppler_path = r'C:\poppler-23.08.0\Library\bin'  # Atualize com o caminho correto
tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'  # Atualize com o caminho correto
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def extract_text(images):
    doc = {
        'extractor': 'pytesseract',
        'pages': [],
    }
    
    # Converter PDF em imagens
    text_ = ""
    for image in images:
        text = pytesseract.image_to_string(image, lang='por').strip()
        doc['pages'].append(text)
        text_+=text
    
    if not text_:
        raise Exception('Não foi possível extrair texto')
    
    return doc

def extract_text_tesseract_pdf_path(pdf_path):
    
    nome_arquivo, extensao = os.path.splitext(os.path.basename(pdf_path))
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    
    doc = extract_text(images)
    doc['filename'] = nome_arquivo + extensao
    
    return doc

def extract_text_tesseract_pdf_bytes(pdf_bytes):
    
    images = convert_from_bytes(pdf_bytes, poppler_path=poppler_path)
    
    # Converter PDF em imagens
    doc = extract_text(images)
    
    return doc

def extract_text_tesseract_image_bytes(img_bytes):
    
    image = Image.open(BytesIO(img_bytes))
    
    # Converter PDF em imagens
    doc = extract_text([image])
    
    return doc