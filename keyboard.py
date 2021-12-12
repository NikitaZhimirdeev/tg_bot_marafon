from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# Объявление кнопок
b1 = KeyboardButton('/liga')
b2 = KeyboardButton('/main_liga')
# Объявления клавиатуры с авторазмером и срытием после нажатия
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# добавление кнопок
kb_client.add(b1).add(b2)