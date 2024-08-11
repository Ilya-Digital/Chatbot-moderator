from typing import Any
from aiogram.utils.keyboard import InlineKeyboardBuilder


def report_kb(message_id, user_id, chat_id) -> Any:
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить сообщение',
                   callback_data=f'delete_msg|{message_id}|{chat_id}')
    builder.button(text='Удалить и забанить',
                   callback_data=f'delete_and_ban|{user_id}|{message_id}|{chat_id}')
    return builder.as_markup()
