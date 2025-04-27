from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class ConversionLog(Base):
    __tablename__ = 'conversion_logs'

    log_id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.document_id'))
    status = Column(String(50), nullable=False)
    conversion_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación
    document = relationship("Document", back_populates="conversion_logs")

    def __repr__(self):
        return f"<ConversionLog(document_id={self.document_id}, status='{self.status}')>"