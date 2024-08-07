import PyPDF2
import os
from io import BytesIO


def process_pdf(file):
    doc = {
        'extractor': 'PyPDF2',
        'pages': [],
    }
    text_ = ""
    reader = PyPDF2.PdfReader(file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text().strip()
        doc['pages'].append(text)
        text_+=text

    if not text_:
        raise Exception('Não foi possível extrair texto do PDF')

    return doc

def extract_text_from_pdf_path(pdf_path):
    
    nome_arquivo, extensao = os.path.splitext(os.path.basename(pdf_path))
    
    with open(pdf_path, 'rb') as file:
        doc = process_pdf(file)
    
    doc['filename'] = nome_arquivo + extensao
    
    return doc

def extract_text_from_pdf_bytes(pdf_bytes):
    # Usando BytesIO para tratar o conteúdo do PDF como um arquivo
    with BytesIO(pdf_bytes) as file_stream:
        doc = process_pdf(file_stream)

    return doc