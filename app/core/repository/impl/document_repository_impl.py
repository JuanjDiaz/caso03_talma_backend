import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.document import Document
from app.core.repository.document_repository import DocumentRepository
from sqlalchemy import select

logger = logging.getLogger(__name__)

class DocumentRepositoryImpl(DocumentRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, doc: Document) -> Document:
        logger.debug(f"Repository saving document {doc.file_name}")
        try:
            self.db.add(doc)
            await self.db.commit()
            await self.db.refresh(doc)
            logger.debug(f"Document {doc.file_name} saved successfully with ID {doc.document_id}")
            return doc
        except Exception as e:
            logger.error(f"Error in repository save for {doc.file_name}: {e}", exc_info=True)
            raise e

    async def find_all(self, skip: int = 0, limit: int = 10) -> list[Document]:
        try:
            query = select(Document).offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}", exc_info=True)
            return []

    async def find_by_id(self, id):
        result = await self.db.execute(
            select(Document).where(Document.document_id == id)
        )
        return result.scalar_one_or_none()

    async def delete(self, id) -> bool:
        doc = await self.find_by_id(id)
        if not doc:
            return False
        try:
            await self.db.delete(doc)
            await self.db.commit()
            return True
        except Exception as e:
             logger.error(f"Error deleting document {id}: {e}", exc_info=True)
             raise e
