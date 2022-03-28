from sqlalchemy import Column, String, Integer

from . import Base


class Document(Base):
    __tablename__ = "document"

    document_id = Column(Integer, primary_key=True, autoincrement=True)
    summary = Column(String, nullable=False)
