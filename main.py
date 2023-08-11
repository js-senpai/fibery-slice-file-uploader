from fastapi import FastAPI
from routes.files_router import files_router

app = FastAPI()
app.include_router(files_router, prefix='/files')