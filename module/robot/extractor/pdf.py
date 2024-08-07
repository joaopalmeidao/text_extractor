import PyPDF2
import os
from io import BytesIO


def extract_text_from_pdf_path(pdf_path):
    
    nome_arquivo, extensao = os.path.splitext(os.path.basename(pdf_path))
    
    doc = {
        'filename': nome_arquivo + extensao,
        'extractor': 'PyPDF2',
        'pages': [],
    }
    text_ = ""
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text().strip()
            doc['pages'].append(text)
            text_+=text

    if not text_:
        raise Exception('Não foi possível extrair texto do PDF')
    
    return doc

def extract_text_from_pdf_bytes(pdf_bytes):
    
    doc = {
        'extractor': 'PyPDF2',
        'pages': [],
    }
    
    # Usando BytesIO para tratar o conteúdo do PDF como um arquivo
    text_ = ""
    with BytesIO(pdf_bytes) as file_stream:
        reader = PyPDF2.PdfReader(file_stream)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text().strip()
            doc['pages'].append(text)
            text_+=text
    
    if not text_:
        raise Exception('Não foi possível extrair texto do PDF')
    
    return doc