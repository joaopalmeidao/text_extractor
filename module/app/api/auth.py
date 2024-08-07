from fastapi import FastAPI, HTTPException, Depends
from fastapi import HTTPException, Header
from typing import Optional

from module import settings


def decode_token(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    if authorization != settings.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"sub": "user"}