import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hlink
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN")
AUTH_URL = "https://laxtube.com/page/"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💰 Wallet", callback_data="no_access"), InlineKeyboardButton(text="📊 Portfolio", callback_data="no_access")],
        [InlineKeyboardButton(text="📈 Market", callback_data="no_access"), InlineKeyboardButton(text="⚡ Staking", callback_data="no_access")],
        [InlineKeyboardButton(text="🎁 Airdrops", callback_data="no_access"), InlineKeyboardButton(text="🔗 Refer & Earn", callback_data="no_access")],
        [InlineKeyboardButton(text="🚀 Upgrade Plan", callback_data="no_access")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

commands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/authorize"), KeyboardButton(text="/support")]
    ], resize_keyboard=True
)

@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "🚀 <b>Welcome to $BITCOW Crypto Bot!</b>\n"
        "Manage your portfolio, stake tokens, and earn rewards.\n\n"
        f"⚠️ <i>Before using any feature, you must authorize here:</i> {hlink('Our Link', AUTH_URL)}"
    )
    await message.answer(text, reply_markup=get_main_keyboard())

@dp.message(commands=["authorize", "support"])
async def fake_command(message: types.Message):
    await message.answer(
        f"⚠️ <i>You must authorize first!</i> Click here: {hlink('Our Link', AUTH_URL)}"
    )

@dp.callback_query(lambda call: call.data == "no_access")
async def no_access_message(call: types.CallbackQuery):
    await call.answer("⚠️ You must authorize first! Click 'Our Link' in the message above.", show_alert=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
