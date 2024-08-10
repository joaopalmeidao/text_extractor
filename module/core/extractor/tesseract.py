import pytesseract
import os
from pdf2image import convert_from_path, convert_from_bytes
from io import BytesIO
from PIL import Image
from platform import system

from module import settings


if settings.SYSTEM == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


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
    if settings.SYSTEM == 'Windows':
        images = convert_from_path(pdf_path, poppler_path=settings.POPPLER_PATH)
    else:
        images = convert_from_path(pdf_path)
    
    doc = extract_text(images)
    doc['filename'] = nome_arquivo + extensao
    
    return doc

def extract_text_tesseract_pdf_bytes(pdf_bytes):
    
    if settings.SYSTEM == 'Windows':
        images = convert_from_bytes(pdf_bytes, poppler_path=settings.POPPLER_PATH)
    else:
        images = convert_from_bytes(pdf_bytes)
    
    # Converter PDF em imagens
    doc = extract_text(images)
    
    return doc

def extract_text_tesseract_image_bytes(img_bytes):
    
    image = Image.open(BytesIO(img_bytes))
    
    # Converter PDF em imagens
    doc = extract_text([image])
    
    return doc