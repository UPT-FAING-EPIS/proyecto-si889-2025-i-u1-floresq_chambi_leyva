from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class DocumentVersion(Base):
    __tablename__ = 'document_versions'

    version_id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.document_id'))
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación
    document = relationship("Document", back_populates="versions")

    def __repr__(self):
        return f"<DocumentVersion(document_id={self.document_id}, version={self.version_number})>"