from fastapi import FastAPI, HTTPException, File, UploadFile
import os

from module.core.customlogger import logger
from module.robot.extractor.pdf import extract_text_from_pdf_bytes
from module.robot.extractor.tesseract import (
    extract_text_tesseract_pdf_bytes,
    extract_text_tesseract_image_bytes
    )
from module.robot.extractor.audio import extract_from_audio
from module.robot.extractor.docx import extract_text_from_docx_bytes

from module import __version__


app = FastAPI(
    title='Api Text Extractor',
    version=__version__,
)

@app.post("/extract/all", 
        description='Extracts text from different extensions file.',
        tags=['Default'])
async def extract_file(file: UploadFile = File(...)):
    
    step = None
    logger.info(f'Processando arquivo: {file.filename}')
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    try:
        extensions = (
            '.pdf',
            
            #audio
            '.mp3',
            '.wav',
            '.ogg',
            '.mp4',
            
            '.docx',
            
            #image
            '.png',
            '.jpg',
            '.jpeg',
        )
        
        step = 'Reading file'
        # Lê o conteúdo do arquivo
        contents = await file.read()
        
        if file.filename.endswith('.pdf'):
            
            try:
                step = 'Processing PDF with PyPDF2'
                response = extract_text_from_pdf_bytes(contents)
            except:
                try:
                    step = 'Processing PDF with pytesseract'
                    response = extract_text_tesseract_pdf_bytes(contents)
                except Exception as e:
                    step = 'Error processing PDF'
                    raise e
        
        elif file.filename.endswith((
            '.mp3',
            '.wav',
            '.ogg',
            '.mp4',
            )):
            step = 'Processing audio'
            response = extract_from_audio(contents, file_extension.replace('.', ''))
            
        elif file.filename.endswith('.docx'):
            step = 'Processing docx'
            response = extract_text_from_docx_bytes(contents)
        
        elif file.filename.endswith((
            '.png',
            '.jpg',
            '.jpeg'
            )):
            step = 'Processing image'
            response = extract_text_tesseract_image_bytes(contents)
        
        else:
            raise Exception(f'Invalid file type. Please upload a file with one of the following extension(s): {extensions}')
        
        return {"filename": file.filename, "content": response}
    
    except Exception as e:
        logger.error(f'Step: {step}\nError: {e}', exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=dict(
                message=str(e),
                step=step,
                class_name=e.__class__.__name__,
                )
            )
    
@app.post("/extract/audio",
        description="Extracts text from an aduio audio file.",
        tags=["Extract"])
async def extract_mp3(file: UploadFile = File(...)):

    logger.info(f'Processing MP3 file: {file.filename}')

    file_extension = os.path.splitext(file.filename)[1].lower()
    
    try:
        extensions = (
            '.mp3',
            '.wav',
            '.ogg',
            '.mp4',
            )
        
        # Read MP3 content
        contents = await file.read()

        if not file.filename.endswith(extensions):
            raise Exception(f'Invalid file type. Please upload an MP3 file with one of the following extension(s): {extensions}')

        response = extract_from_audio(contents, file_extension.replace('.', ''))
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
