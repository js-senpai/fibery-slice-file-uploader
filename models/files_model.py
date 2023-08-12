import uuid as uuid_pkg
import sqlalchemy
from sqlalchemy import Column
from configs.db_config import Base


class FilesModel(Base):
    __tablename__ = "files"
    id = Column("id", sqlalchemy.String(36), primary_key=True, default=lambda: str(uuid_pkg.uuid4()))
    file_id = Column("file_id", sqlalchemy.String(36), nullable=False, index=True)