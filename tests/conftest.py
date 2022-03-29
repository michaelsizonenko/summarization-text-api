import os
import sys
import asyncio
import pytest

from unittest.mock import AsyncMock
from starlette.testclient import TestClient

from app.services.summary_text_service import SummaryTextService
from main import app
from app.routers import document

app.include_router(document.router)

app.state.db = AsyncMock()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

app.include_router(document.router)

app.state.db = AsyncMock()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> TestClient:
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session")
def summary_text_service():
    return SummaryTextService(doc_repo=AsyncMock())

