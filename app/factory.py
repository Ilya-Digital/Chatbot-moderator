from aiogram.filters.callback_data import CallbackData


class DelMsg(CallbackData, prefix="delete_msg"):
    message_id: int
    chat_id: int


class DelAndBan(CallbackData, prefix="delete_and_ban"):
    user_id: int
    message_id: int
    chat_id: int