import httpx
from sqlalchemy import select, insert
from fastapi import HTTPException, APIRouter

from configs.db_config import db_engine
from configs.envs_config import APP_TOKEN
from configs.logger_config import logger
from models import files_model
from schemas.files_info_schema import FileInfoModel

files_router = APIRouter()

@files_router.post("/")
async def upload_file(file_info: FileInfoModel):
    try:
        if file_info.app_token != APP_TOKEN:
            raise HTTPException(status_code=403, detail="You sent an unknown token")
        async with httpx.AsyncClient() as client:
            headers_fibery = {
                "Authorization": f"Token {file_info.fibery_token}"
            }
            for item in file_info.files:
                query = select(files_model).where(files_model.c.file_id == item.file_id)
                result = await db_engine.execute(query)
                rows = result.fetchall()
                if len(rows) == 0:
                    response_fibery = await client.get(item.file_url, headers=headers_fibery)
                    if response_fibery.status_code != 200:
                        raise HTTPException(status_code=response_fibery.status_code, detail="Error getting the file")

                    form_data = {
                        'name': item.file_name,
                        'file': (item.file_name, response_fibery.content, "application/octet-stream")
                    }

                    headers = {
                        "Authorization": f"Bearer {file_info.super_dispatch_token}"
                    }
                    response = await client.post(file_info.super_dispatch_url, headers=headers, files=form_data)
                    if response.status_code != 200:
                        raise HTTPException(status_code=response.status_code, detail="Error uploading the file")

                    save_data = insert(files_model).values(file_id=item.file_id)
                    await db_engine.execute(save_data)

        return { 'ok': 'The request has been successfully completed' }
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise HTTPException(status_code=400, detail=str(e))