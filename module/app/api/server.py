from fastapi import FastAPI, HTTPException, File, UploadFile

from module.core.customlogger import logger
from module.robot.extractor.pdf import extract_text_from_pdf_bytes
from module.robot.extractor.tesseract import extract_text_tesseract_pdf_bytes
from module.robot.extractor.audio import extract_from_audio_mp3

from module import __version__

from .auth import decode_token


app = FastAPI(
    title='Api Text Extractor',
    version=__version__,
)

@app.post("/extract", 
        description='Recebe um arquivo de qualquer extensão e realiza extração de texto.',
        tags=['Extract'])
async def extract_file(file: UploadFile = File(...)):
    
    logger.info(f'Processando arquivo: {file.filename}')
    
    try:
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
        
        else:
            # Adicione outros tipos de arquivo se necessário
            return {"error": "Tipo de arquivo não suportado"}
        
        return {"filename": file.filename, "content": response}
    
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail='Erro ao processar o arquivo')

