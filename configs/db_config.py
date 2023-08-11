from sqlalchemy import MetaData, create_engine

from configs.envs_config import DATABASE_URL

db_metadata = MetaData()
db_engine = create_engine(
    DATABASE_URL
)
db_metadata.create_all(db_engine)