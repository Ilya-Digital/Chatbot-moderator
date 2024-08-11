import re
import asyncio
from typing import Any
from datetime import datetime, timedelta
from contextlib import suppress


from aiogram import types, Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile, ChatPermissions
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
import pymorphy3


import app.keyboards as kb


user = Router()

morph = pymorphy3.MorphAnalyzer(lang='ru')
triggers = ['клоун']


@user.message(Command('report'))
async def report(message: Message, bot: Bot, command: CommandObject) -> Any:
    reply = message.reply_to_message
    if not reply:
        return await message.reply('👀 Пользователь не найден!')
    with suppress(TelegramBadRequest):
        time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(time)
        await bot.forward_message(
            chat_id=123, from_chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id
        )
        print(reply.chat.id)
        await bot.send_message(chat_id=123, text=f'👆 Дата: {time}\n\nUser_id: {reply.from_user.id}\n\nЗапись: {command.args}', reply_markup=kb.report_kb(reply.message_id, reply.from_user.id, reply.chat.id))


@user.callback_query(F.data.startswith('delete_msg'))
async def delete_msg(callback: CallbackQuery, bot: Bot) -> None:
    # print(callback.data.split('|'))
    message_id = callback.data.split('|')[1]
    chat_id = callback.data.split('|')[2]
    await bot.delete_message(int(chat_id), int(message_id))


@user.callback_query(F.data.startswith('delete_and_ban'))
async def delete_msg(callback: CallbackQuery, bot: Bot) -> Any:
    user_id = callback.data.split('|')[1]
    message_id = callback.data.split('|')[2]
    chat_id = callback.data.split('|')[3]
    await bot.delete_message(int(chat_id), int(message_id))
    await bot.ban_chat_member(int(chat_id), int(user_id))


@user.message(F.text)
async def profinity_filter(message: Message) -> Any:
    for word in message.text.strip().lower().split():
        if word in triggers:
            parsed_word = morph.parse(word)[0]
            normal_form = parsed_word.normal_form
            for trigger in triggers:
                if trigger in normal_form:
                    return await message.reply('🤬 Не ругайся!')
