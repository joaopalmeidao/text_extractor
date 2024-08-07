import pytesseract
import os
from pdf2image import convert_from_path, convert_from_bytes
from io import BytesIO

poppler_path = r'C:\poppler-23.08.0\Library\bin'  # Atualize com o caminho correto
tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'  # Atualize com o caminho correto
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def extract_text_tesseract_pdf_path(pdf_path):
    
    nome_arquivo, extensao = os.path.splitext(os.path.basename(pdf_path))
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    
    doc = {
        'filename': nome_arquivo + extensao,
        'pages': [],
        'extractor': 'pytesseract',
    }
    
    text_ = ""
    for image in images:
        text = pytesseract.image_to_string(image, lang='por').strip()
        doc['pages'].append(text)
        text_+=text
    
    if not text_:
        raise Exception('Não foi possível extrair texto do PDF')
    
    return doc

def extract_text_tesseract_pdf_bytes(pdf_bytes):
    
    images = convert_from_bytes(pdf_bytes, poppler_path=poppler_path)
    
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
        raise Exception('Não foi possível extrair texto do PDF')
    
    return doc