from typing import Any
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.factory import DelMsg, DelAndBan


def report_kb(message_id, user_id, chat_id) -> Any:
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить сообщение',
                   callback_data=DelMsg(
                       message_id=message_id,
                       chat_id=chat_id
                   ))
    builder.button(text='Удалить и забанить',
                   callback_data=DelAndBan(
                       user_id=user_id,
                       message_id=message_id,
                       chat_id=chat_id
                   ))
    return builder.as_markup()
