from pydantic import BaseModel, Field
from typing import List, Dict, Any


class ContentModel(BaseModel):
    pages: List[str] = Field(..., description="List of extracted text pages")

class ExtractResponse(BaseModel):
    filename: str = Field(..., description="The name of the uploaded file")
    content: ContentModel = Field(..., description="Content extracted from the file")

# Modelo de resposta para o código 422
class ValidationErrorResponse(BaseModel):
    detail: List[Dict[str, Any]] = Field(..., description="Details of the validation error")