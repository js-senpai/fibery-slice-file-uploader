import json
import os

import httpx
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from configs.db_config import get_db
from configs.envs_config import APP_TOKEN
from configs.logger_config import logger
from models.files_model import FilesModel
from schemas.files_info_schema import  FileInfoSchema
import mimetypes
files_router = APIRouter()

@files_router.post("/")
async def upload_file(file_info: FileInfoSchema,db: Session = Depends(get_db)):
    if file_info.app_token != APP_TOKEN:
        raise HTTPException(status_code=403, detail="You sent an unknown token")

    async with httpx.AsyncClient() as client:
        headers_fibery = {
            "Authorization": f"Token {file_info.fibery_token}"
        }
        responses = []
        for item in file_info.files:
            get_files = db.query(FilesModel).where(FilesModel.file_id == item.file_id).all()
            if len(get_files) == 0:
                response_fibery = await client.get(item.file_url, headers=headers_fibery)
                if response_fibery.status_code != 200 and response_fibery.status_code != 201:
                    logger.error(f"The error in getting the file. Status code {response_fibery.status_code}")
                    raise HTTPException(status_code=400,
                                        detail=f"The error in getting the file. Status code {response_fibery.status_code}")
                file_content = response_fibery.content
                file_name = os.path.splitext(item.file_name)[0].replace(" ", "_").strip()
                file_extension = item.file_name.split('.')[-1]
                file_type, _ = mimetypes.guess_type(f"dummy.{file_extension}")
                if file_type is None:
                    file_type = "application/octet-stream"
                form_data = {
                    "file": (file_name, file_content, file_type)
                }
                json_data = {
                    "name": file_name
                }
                headers = {
                    "Authorization": f"Bearer {file_info.super_dispatch_token}"
                }
                response = await client.post(file_info.super_dispatch_url, headers=headers, files=form_data, data=json_data)
                read_response = json.loads(response.content)
                if read_response['meta']['code'] != 200 and read_response['meta']['code'] != 201:
                    logger.error(f"The error in uploading the file. Status code {read_response['meta']['code']}. Error message {str(read_response['error'])}")
                    raise HTTPException(status_code=400, detail=f"The error in uploading the file. Status code {read_response['meta']['code']}. Error message {str(read_response['error'])}")
                db_file = FilesModel(file_id=item.file_id)
                db.add(db_file)
                db.commit()
                db.refresh(db_file)
                responses.append(read_response)

    return {'ok': responses}
