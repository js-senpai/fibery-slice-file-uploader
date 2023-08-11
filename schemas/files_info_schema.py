from pydantic import BaseModel, HttpUrl
from typing import List
class FilesModel(BaseModel):
    file_name: str
    file_url: str
    file_id: str


class FileInfoModel(BaseModel):
    fibery_token: str
    app_token: str
    super_dispatch_token: str
    super_dispatch_url: HttpUrl
    files: List[FilesModel]