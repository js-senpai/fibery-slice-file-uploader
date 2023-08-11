import uuid
import sqlalchemy

from configs.db_config import db_metadata

files_model = sqlalchemy.Table(
    "files",
    db_metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True, default=str(uuid.uuid4())),
    sqlalchemy.Column("file_id", sqlalchemy.String, nullable=False, index=True)
)