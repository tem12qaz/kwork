import io
import os
import asyncio
import traceback

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS
from kewboards import get_keywords_keyboard, get_main_keyboard, main_callback, cancel_keyboard
from models import TelegramUser, Keyword
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        user = await TelegramUser.create(
            telegram_id=message.from_user.id, username=message.from_user.username
        )

    if int(user.telegram_id) not in ADMINS:
        return

    await message.answer(
        'Бот Kwork',
        reply_markup=get_main_keyboard(user)
    )
    return


@dp.callback_query_handler(main_callback.filter())
async def main_menu(callback: types.CallbackQuery, callback_data):
    user = await TelegramUser.get_or_none(telegram_id=callback.from_user.id)
    if user is None or int(user.telegram_id) not in ADMINS:
        return

    select = callback_data.get('select')

    if select == 'add':
        user.state = f'{callback.message.message_id}'
        await user.save()
        await callback.message.edit_text(
            'Введите слово',
            reply_markup=cancel_keyboard
        )
    elif select == 'cancel':
        user.state = ''
        await user.save()
        await callback.message.edit_text(
            'Бот Kwork',
            reply_markup=get_main_keyboard(user)
        )
    elif select == 'stop':
        user.active = False
        await user.save()
        await callback.message.edit_text(
            'Бот Kwork',
            reply_markup=get_main_keyboard(user)
        )
    elif select == 'start':
        user.active = True
        await user.save()
        await callback.message.edit_text(
            'Бот Kwork',
            reply_markup=get_main_keyboard(user)
        )
    elif select == 'remove':
        await callback.message.edit_text(
            'Нажмите на слово для удаления',
            reply_markup=await get_keywords_keyboard(user)
        )
    elif 'remove' in select:
        id_ = int(select.split('_')[1])
        keyword = await Keyword.get_or_none(id=id_)
        if not keyword:
            await callback.message.edit_text(
                'Нажмите на слово для удаления',
                reply_markup=await get_keywords_keyboard(user)
            )
        elif await keyword.owner != user:
            await callback.message.edit_text(
                'Нажмите на слово для удаления',
                reply_markup=await get_keywords_keyboard(user)
            )
        else:
            await keyword.delete()
            await callback.answer('Слово удалено')
            await callback.message.edit_text(
                'Нажмите на слово для удаления',
                reply_markup=await get_keywords_keyboard(user)
            )
    await callback.answer()
    return


@dp.message_handler()
async def listen_handler(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None or int(user.telegram_id) not in ADMINS:
        return
    await message.delete()

    if not user.state:
        return
    try:
        await bot.delete_message(user.telegram_id, int(user.state))
    except:
        pass

    await Keyword.create(owner=user, text=message.text)
    await message.answer('Слово добавлено', reply_markup=get_main_keyboard())

