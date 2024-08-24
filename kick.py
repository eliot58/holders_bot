import asyncio
from aiogram import Bot
from tortoise import Tortoise, run_async
from tortoise.transactions import in_transaction
from src.holder.utils import check_nft
from src.holder.models import Holder
from src.config.settings import DATABASE_URI, BOT_TOKEN, CHAT_ID, APPS_MODELS

bot = Bot(token=BOT_TOKEN)

async def kick_user_from_chat(user_id: int):
    try:
        await bot.ban_chat_member(chat_id=CHAT_ID, user_id=user_id)
        print(f"User {user_id} kicked from chat.")
    except Exception as e:
        print(f"Failed to kick user {user_id}: {e}")

async def check_and_kick_users():
    async with in_transaction():
        holders = await Holder.all()
        for holder in holders:
            if await check_nft(holder.address):
                user_id = int(holder.id)
                await kick_user_from_chat(user_id)
                await holder.delete()

async def run():
    await Tortoise.init(db_url=DATABASE_URI, modules={"models": APPS_MODELS})
    await check_and_kick_users()
    await Tortoise.close_connections()

async def periodic_task(interval: int):
    while True:
        await run()
        await asyncio.sleep(interval)

if __name__ == "__main__":
    run_async(periodic_task(2 * 60 * 60))  # 2 hours in seconds
