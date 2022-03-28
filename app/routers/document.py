from typing import List

from fastapi import APIRouter, Depends

from app.schemas.document import DocumentResponse, DocumentBase, DocumentCreate
from app.services.db.document_repo import DocumentRepository
from app.services.summary_text_service import SummaryTextService
from context import get_doc_repo, get_summary_text_service

router = APIRouter()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int,
                       doc_repo: DocumentRepository = Depends(get_doc_repo)):
    return await doc_repo.get(document_id=document_id)


@router.get("/list/", response_model=List[DocumentResponse])
async def get_documents(doc_repo: DocumentRepository = Depends(get_doc_repo)):
    return await doc_repo.get_all()


@router.post("/create", response_model=DocumentBase)
async def create_document(document: DocumentCreate,
                          summary_text_service: SummaryTextService = Depends(get_summary_text_service)):
    return await summary_text_service.create_document(text=document.text)
