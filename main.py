from fastapi import FastAPI,status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from configs.db_config import Base, engine
from routes.files_router import files_router

app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
app.include_router(files_router, prefix='/api/files')

Base.metadata.create_all(bind=engine)