import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram import types
from src.config.settings import APPS_MODELS, BOT_TOKEN, DATABASE_URI, CHAT_ID
from tortoise import Tortoise, run_async
from src.holder.models import Holder

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    buttons = [
        [
            types.InlineKeyboardButton(text="connect", web_app=types.WebAppInfo(url="https://holder.notwise.co/"))
        ]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Connect wallet", reply_markup=markup)


@dp.message(Command("get"))
async def command_get_handler(message: types.Message) -> None:
    await message.answer((await message.bot.create_chat_invite_link(chat_id=CHAT_ID, creates_join_request=True)).invite_link)


@dp.chat_join_request()
async def user_joined_chat(message: types.Message):
    holder = await Holder.get_or_none(id=message.from_user.id)
    if holder:
        message.bot.approve_chat_join_request(chat_id=CHAT_ID, user_id=message.from_user.id)
    else:
        message.bot.decline_chat_join_request(chat_id=CHAT_ID, user_id=message.from_user.id)
    


async def main() -> None:
    await Tortoise.init(db_url=DATABASE_URI, modules={"models": APPS_MODELS})
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run_async(main())