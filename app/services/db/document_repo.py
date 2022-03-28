from typing import List

from databases import Database
from sqlalchemy import select, insert
from fastapi import HTTPException
from starlette import status

from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentBase


class DocumentNotFound(HTTPException):
    def __init__(self, document_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Document not found: {document_id}")


class DocumentCreateError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Document create error")


class DocumentRepository:

    def __init__(self, db: Database):
        self.db = db

    async def get(self, document_id: int) -> DocumentResponse:
        query = select([Document]).where(Document.document_id == document_id)

        result = await self.db.fetch_one(query=query)

        if not result:
            raise DocumentNotFound(document_id=document_id)

        return DocumentResponse.parse_obj(result)

    async def get_all(self) -> List[DocumentResponse]:
        query = select([Document])
        result = await self.db.fetch_all(query=query)
        return [DocumentResponse.parse_obj(document) for document in result if document]

    async def add(self, summary: str) -> DocumentBase:

        async with self.db.transaction():

            stmt = (
                insert(Document).values(summary=summary).returning(Document.document_id)
            )
            document_id = await self.db.execute(query=stmt)
            if not document_id:
                raise DocumentCreateError()

            return DocumentBase(document_id=document_id)
