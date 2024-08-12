import re
import asyncio
from typing import Any
from contextlib import suppress
from datetime import datetime, timedelta


from aiogram import types, Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile, ChatPermissions
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
import pymorphy3


import app.keyboards as kb
from config import ADMIN_ID

admin = Router()
admin.message.filter(F.chat.type == 'supergroup', F.from_user.id == ADMIN_ID)


def parse_time(time_string: str | None) -> datetime | None:
    if not time_string:
        return None
    match_ = re.match(r"(\d+)([a-z])", time_string.lower().strip())
    current_datetime = datetime.now()
    if match_:
        value, unit = int(match_.group(1)), match_.group(2)

        match unit:
            case "h":
                time_delta = timedelta(hours=value)
            case "d":
                time_delta = timedelta(days=value)
            case "w":
                time_delta = timedelta(weeks=value)
            case _:
                return None
    else:
        return None

    new_datetime = current_datetime + time_delta
    return new_datetime


@admin.message(Command('ban'))
async def ban(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    reply = message.reply_to_message
    if not reply:
        return await message.reply('👀 Пользователь не найден!')

    until_date = parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(
            chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date
        )
        await message.reply(f'⛔ Пользователь <b>{mention}</b> был забанен!', parse_mode="HTML")


@admin.message(Command('mute'))
async def mute(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    reply = message.reply_to_message
    if not reply:
        return await message.reply('👀 Пользователь не найден!')

    until_date = parse_time(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            until_date=until_date,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.reply(f'🔇 Пользователь <b>{mention}</b> был заглушён!', parse_mode="HTML")
