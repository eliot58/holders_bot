from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import DATABASE_URI, APPS_MODELS
from tortoise.contrib.fastapi import RegisterTortoise
from src.holder.router import router as holder_router
from fastapi import FastAPI


@asynccontextmanager 
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url=DATABASE_URI,
        modules={"models": APPS_MODELS}
    ):
        yield

app = FastAPI(
    title="Holder",
    docs_url="/",
    lifespan=lifespan
)


app.include_router(holder_router)


origins = ['*']
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                "Authorization"],
)
