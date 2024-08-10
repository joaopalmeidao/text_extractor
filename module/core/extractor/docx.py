from docx import Document
import os
from io import BytesIO


def process_docx(file) -> str:
    
    doc = {
        'extractor': 'docx',
        'pages': [],
    }
    text_ = ""
    document = Document(file)

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        text_+=text + '\n'
    
    doc['pages'].append(text_)
    
    if not text_:
        raise Exception('Não foi possível extrair texto')
    
    return doc

def extract_text_from_docx_path(pdf_path):
    
    nome_arquivo, extensao = os.path.splitext(os.path.basename(pdf_path))
    
    with open(pdf_path, 'rb') as file:
        doc = process_docx(file)
    
    doc['filename'] = nome_arquivo + extensao
    
    return doc

def extract_text_from_docx_bytes(pdf_bytes):
    # Usando BytesIO para tratar o conteúdo do PDF como um arquivo
    with BytesIO(pdf_bytes) as file_stream:
        doc = process_docx(file_stream)

    return doc
