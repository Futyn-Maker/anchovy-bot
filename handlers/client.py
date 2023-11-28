from datetime import datetime
import pytz

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot import db, dp

from responses.client_responses import CLIENT_RESPONSES
from responses.keyboards import ASK_KEYBOARD


moscow_tz = pytz.timezone("Europe/Moscow")

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(text=CLIENT_RESPONSES["start"], reply_markup=ASK_KEYBOARD)


@dp.message_handler(commands="help")
async def show_help(message: types.Message):
    await message.answer(text=CLIENT_RESPONSES["help"])


@dp.message_handler(commands="ask")
async def ask(message: types.Message):
    await message.answer(text=CLIENT_RESPONSES["ask"], reply_markup=ASK_KEYBOARD)


@dp.message_handler()
async def save_message(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        first_name, last_name = message.from_user.first_name, message.from_user.last_name
        if first_name and last_name:
            name = f"{first_name} {last_name}"
        elif firstname:
            name = first_name
        else:
            name = None
        user = await db.add_user(message.from_user.id, message.from_user.username, name)
    current_time = datetime.now(moscow_tz)
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    await db.add_response(user["id"], timestamp, message.text)
    await message.answer(CLIENT_RESPONSES["message_saved"])