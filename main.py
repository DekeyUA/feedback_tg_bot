import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart


from bot.handlers import router
current_script_path = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_script_path,'.env')

load_dotenv(dotenv_path)

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def start_message(message: Message):
    await message.answer("Hel0")

@dp.message(lambda m: m.chat.type == "private")
async def all_messages(message: Message):
    user_id = message.from_user.id
    answer = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Reply", callback_data=f"reply_message_{user_id}"),
         InlineKeyboardButton(text="Dimon", callback_data=f"dimon_{user_id}")]
    ])
    await message.bot.send_message(os.getenv("owner_id"), f"Повідомлення від {message.from_user.first_name}: \n\n"
                                                          f"{message.text}", reply_markup=answer)

async def start_bot(bot: Bot):
    await bot.send_message(os.getenv("owner_id"), f'Бот запущен')

async def stop_bot(bot: Bot):
    await bot.send_message(os.getenv("owner_id"), f'Бот остановлен')

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Game Over!')