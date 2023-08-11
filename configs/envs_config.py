import os

from dotenv import load_dotenv

# LOAD ENV
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", None)
APP_TOKEN = os.getenv("APP_TOKEN", None)