import PyPDF2
import os
from io import BytesIO
import fitz  # PyMuPDF

from . import tesseract


def has_images(page):
    """Verifica se uma página contém imagens."""
    images = page.get_images(full=True)
    return len(images) > 0

def extract_images_from_page(page):
    """Extrai imagens de uma página PDF."""
    image_list = page.get_images(full=True)
    images = []
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = page.document.extract_image(xref)
        image_bytes = base_image["image"]
        images.append(image_bytes)
    return images

def process_pdf(file):
    doc = {
        'extractor': 'PyPDF2',
        'pages': [],
    }
    
    reader = PyPDF2.PdfReader(file)
    
    file.seek(0)
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    
    text_ = ""
    for page_num in range(len(reader.pages)):
        
        fitz_page = pdf_document[page_num]
        if has_images(fitz_page):
            print('Tem imagem')
            doc['extractor'] = 'PyPDF2+tesseract'
            file.seek(0)  # Reseta o ponteiro para o início do arquivo
            images = images = tesseract.convert_from_bytes(file.read(), first_page=page_num+1, last_page=page_num+1)
            text = tesseract.extract_text(images)
            doc['pages'].append(text)
            text_ += text
            
        else:
            page = reader.pages[page_num]
            text = page.extract_text().strip()
            doc['pages'].append(text)
            text_+=text

    if not text_:
        raise Exception('Não foi possível extrair texto do PDF')

    return doc

# def process_pdf(file):
#     doc = {
#         'extractor': 'PyPDF2',
#         'pages': [],
#     }
    
#     text_ = ""
#     reader = PyPDF2.PdfReader(file)
#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]
#         text = page.extract_text().strip()
#         doc['pages'].append(text)
#         text_+=text

#     if not text_:
#         raise Exception('Não foi possível extrair texto do PDF')

#     return doc

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