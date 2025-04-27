from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Document(Base):
    __tablename__ = 'documents'

    document_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String(255), nullable=False)
    original_format = Column(String(20), nullable=False)
    markdown_content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document")
    conversion_logs = relationship("ConversionLog", back_populates="document")

    def __repr__(self):
        return f"<Document(title='{self.title}', format='{self.original_format}')>"