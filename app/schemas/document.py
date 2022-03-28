
from pydantic import BaseModel


class DocumentBase(BaseModel):
    document_id: int


class DocumentResponse(DocumentBase):
    summary: str


class DocumentCreate(BaseModel):
    text: str
