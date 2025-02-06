import logging
from dotenv import load_dotenv
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKING_BASE = "./working"

print(load_dotenv(os.path.join(PROJECT_ROOT, "../../.env")))
logging.debug(
    "LOAD ENV FROM FILE: ", load_dotenv(os.path.join(PROJECT_ROOT, "../../.env"))
)

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL") if os.getenv("LOGGING_LEVEL") else "INFO"

# APP SETTINGS
API_PREFIX = os.getenv("API_PREFIX")
ENDPOINT_PREFIX = "/endpoints"

API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

# AUTH SETTINGS
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

SUPER_LOGIN = os.getenv("SUPER_LOGIN")
SUPER_PASSWORD = os.getenv("SUPER_PASSWORD")


# TG SETTINGS
USE_TG_WEBHOOK = os.getenv("USE_TG_WEBHOOK") == "true"
TG_WEBHOOK_URL = f"https://{API_HOST}:{API_PORT}/tg"

# LLM SETTINGS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DB POSTGRES SETTINGS
DATABASE_URL = os.getenv("DATABASE_URL")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


# REDI SETTINGS
REDIS_URL = os.getenv("REDIS_URL")
HISTORY_TOKEN_CAPACITY = int(os.getenv("HISTORY_TOKEN_CAPACITY"))

# S3 SETTINGS
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
MINIO_URL = os.getenv("MINIO_URL")


CONTAINER_NAME = os.getenv("COOLIFY_CONTAINER_NAME")
if CONTAINER_NAME == "":
    print("COOLIFY_CONTAINER_NAME is not set")
