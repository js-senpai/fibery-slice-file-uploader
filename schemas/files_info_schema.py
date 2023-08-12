from pydantic import BaseModel
from typing import List
class FilesListSchema(BaseModel):
    file_name: str
    file_url: str
    file_id: str
class FileInfoSchema(BaseModel):
    fibery_token: str
    app_token: str
    super_dispatch_token: str
    super_dispatch_url: str
    files: List[FilesListSchema]
