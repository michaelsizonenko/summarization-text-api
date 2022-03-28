from databases import Database
from fastapi import Depends

from app.db.connection import get_database
from app.services.db.document_repo import DocumentRepository
from app.services.summary_text_service import SummaryTextService


def get_doc_repo(database: Database = Depends(get_database)) -> DocumentRepository:
    return DocumentRepository(db=database)


def get_summary_text_service(doc_repo: DocumentRepository = Depends(get_doc_repo)):
    return SummaryTextService(doc_repo=doc_repo)
