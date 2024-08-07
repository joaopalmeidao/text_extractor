from fastapi import FastAPI, HTTPException, File, UploadFile

from module.core.customlogger import logger
from module.robot.extractor.pdf import extract_text_from_pdf_bytes
from module.robot.extractor.tesseract import (
    extract_text_tesseract_pdf_bytes,
    extract_text_tesseract_image_bytes
    )
from module.robot.extractor.audio import extract_from_audio_mp3
from module.robot.extractor.docx import extract_text_from_docx_bytes

from module import __version__

from .auth import decode_token


app = FastAPI(
    title='Api Text Extractor',
    version=__version__,
)

@app.post("/extract/all", 
        description='Extracts text from different extensions file.',
        tags=['Default'])
async def extract_file(file: UploadFile = File(...)):
    
    logger.info(f'Processando arquivo: {file.filename}')
    
    try:
        extensions = (
            '.pdf',
            
            '.mp3',
            
            '.docx',
            
            '.png',
            '.jpg',
            '.jpeg',
        )
        
        # Lê o conteúdo do arquivo
        contents = await file.read()
        
        if file.filename.endswith('.pdf'):
            
            try:
                response = extract_text_from_pdf_bytes(contents)
            except:
                try:
                    response = extract_text_tesseract_pdf_bytes(contents)
                except Exception as e:
                    raise e
        
        elif file.filename.endswith('.mp3'):
            response = extract_from_audio_mp3(contents)
            
        elif file.filename.endswith('.docx'):
            response = extract_text_from_docx_bytes(contents)
        
        elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
            response = extract_text_tesseract_image_bytes(contents)
        
        else:
            raise Exception(f'Invalid file type. Please upload a file with one of the following extension(s): {extensions}')
        
        return {"filename": file.filename, "content": response}
    
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/extract/mp3",
        description="Extracts text from an MP3 audio file.",
        tags=["Extract"])
async def extract_mp3(file: UploadFile = File(...)):

    logger.info(f'Processing MP3 file: {file.filename}')

    try:
        extensions = ('.mp3')
        
        # Read MP3 content
        contents = await file.read()

        if not file.filename.endswith(extensions):
            raise Exception(f'Invalid file type. Please upload an MP3 file with one of the following extension(s): {extensions}')

        response = extract_from_audio_mp3(contents)
        return {"filename": file.filename, "content": response}

    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/pdf/pypdf2",
        description="Extracts text from a PDF using PyPDF2 library.",
        tags=["Extract"])
async def extract_pdf_pypdf2(file: UploadFile = File(...)):

    logger.info(f'Processing PDF file (PyPDF2): {file.filename}')

    try:
        extensions = ('.pdf')
        
        # Read PDF content
        contents = await file.read()

        if not file.filename.endswith(extensions):
            raise Exception(f'Invalid file type. Please upload a PDF file with one of the following extension(s): {extensions}')

        response = extract_text_from_pdf_bytes(contents)
        return {"filename": file.filename, "content": response}

    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/pdf/tesseract",
        description="Extracts text from a PDF using Tesseract library",
        tags=["Extract"])
async def extract_pdf_tesseract(file: UploadFile = File(...)):

    logger.info(f'Processing PDF file (Tesseract): {file.filename}')

    try:
        extensions = ('.pdf')
        
        # Read PDF content
        contents = await file.read()

        if not file.filename.endswith(extensions):
            raise Exception(f'Invalid file type. Please upload a PDF file with one of the following extension(s): {extensions}')

        response = extract_text_tesseract_pdf_bytes(contents)
        return {"filename": file.filename, "content": response}

    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/extract/docx",
        description="Extracts text from a Docx using Docx library",
        tags=["Extract"])
async def extract_docx(file: UploadFile = File(...)):

    logger.info(f'Processing Docx file (Docx): {file.filename}')

    try:
        extensions = ('.docx')
        
        # Read PDF content
        contents = await file.read()

        if not file.filename.endswith(extensions):
            raise Exception(f'Invalid file type. Please upload a Docx file with one of the following extension(s): {extensions}')

        response = extract_text_from_docx_bytes(contents)
        return {"filename": file.filename, "content": response}

    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/image",
        description="Extracts text from a image using Tesseract library",
        tags=["Extract"])
async def extract_image_text(file: UploadFile = File(...)):
    try:
        extensions = ('.png', '.jpg', '.jpeg')
        
        contents = await file.read()

        if not file.filename.endswith(extensions):
            raise Exception(f'Invalid file type. Please upload a image file with one of the following extension(s): {extensions}')

        text = extract_text_tesseract_image_bytes(contents)
        return {"filename": file.filename, "content": text}
    
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
