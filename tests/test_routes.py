from unittest.mock import patch

from app.schemas.document import DocumentResponse, DocumentBase
from app.services.db.document_repo import DocumentRepository
from app.services.summary_text_service import SummaryTextService


@patch.object(DocumentRepository, 'get_all')
def test_get_all(doc_repo, client):
    doc_repo.return_value = [DocumentResponse(document_id=1, summary="something")]
    DocumentResponse(document_id=1, summary="test")
    response = client.get("/document/list/")

    assert response.status_code == 200
    assert response.json() == [{"document_id": 1, "summary": "something"}]


@patch.object(DocumentRepository, 'get')
def test_get_document(doc_repo, client):
    doc_repo.return_value = DocumentResponse(document_id=1, summary="test")
    response = client.get("/document/1")

    assert response.status_code == 200
    assert response.json() == {'document_id': 1, 'summary': 'test'}


@patch.object(SummaryTextService, 'create_document')
def test_create_document(doc_repo, client):
    data = {"text": "Very long text"}
    doc_repo.return_value = DocumentBase(document_id=1)
    response = client.post("/document/create", json=data)

    assert response.status_code == 200
    assert response.json() == {'document_id': 1}
