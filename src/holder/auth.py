from datetime import timedelta
from fastapi import HTTPException
from src.config.settings import BOT_TOKEN
from src.tma.errors import ExpiredError
from src.tma.validate import validate
from src.tma.parse import parse



async def get_userId(initData: str):
    try:
        validate(initData, BOT_TOKEN, timedelta(minutes=5).seconds)
        
    except ExpiredError:
        raise HTTPException(
            status_code=400,
            detail=f"init data expired {initData}",
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid init data {initData}",
        )
    else:
        chat = parse(initData)
        return str(chat.user.id)