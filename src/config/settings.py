import os
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = '-1002234423310'

BOT_TOKEN = os.environ.get("BOT_TOKEN")

TONAPI = os.environ.get("TONAPI")

DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/' \
               f'{os.environ.get("POSTGRES_DB")}'

COLLECTION = os.environ.get("COLLECTION")

APPS_MODELS = [
    "src.holder.models",
    "aerich.models"
]