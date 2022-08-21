from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from models import TelegramUser

main_callback = CallbackData("main_menu", 'select')


def get_main_keyboard(user: TelegramUser):
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Добавить слово',
                                 callback_data=main_callback.new(select='add'))
        ],
        [
            InlineKeyboardButton(text='Удалить слово',
                                 callback_data=main_callback.new(select='remove'))
        ]
    ]
    if user.active:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='Остановить парсинг',
                                     callback_data=main_callback.new(select='stop'))
            ]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='Возобновить парсинг',
                                     callback_data=main_callback.new(select='start'))
            ]
        )
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )
    return keyboard


async def get_keywords_keyboard(user: TelegramUser):
    inline_keyboard = []
    keywords = await user.keywords.all()
    for i in range(0, len(keywords), 2):
        if i != len(keywords)-1:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(text=f'{keywords[i].text}',
                                         callback_data=main_callback.new(select=f'remove_{keywords[i].id}')),
                    InlineKeyboardButton(text=f'{keywords[i+1].text}',
                                         callback_data=main_callback.new(select=f'remove_{keywords[i+1].id}')),
                ]
            )
        else:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(text=f'{keywords[i].text}',
                                         callback_data=main_callback.new(select=f'remove_{keywords[i].id}'))
                ]
            )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text='Закрыть меню',
                                 callback_data=main_callback.new(select='cancel'))
        ]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return keyboard

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена',
                                 callback_data=main_callback.new(select='cancel'))
        ]
    ]
)
