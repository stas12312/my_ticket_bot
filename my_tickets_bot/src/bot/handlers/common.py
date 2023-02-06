"""Роутер с общими обработчиками"""
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from services.repositories import Repo
from ..callbacks import CloseCallback
from ..commands import AppCommand as MyCommand
from ..keybaords import get_menu_keyboard


async def start_handler(
        message: types.Message,
        repo: Repo,
):
    """Обработчик команды /start"""

    keyboard = get_menu_keyboard()

    user = message.from_user

    await repo.user.save(user.id, user.username)

    await message.answer(
        text='Приветствуем в "Мои билеты"',
        reply_markup=keyboard,
    )


async def close_menu(
        query: types.CallbackQuery,
):
    """Закрытие меню"""
    await query.message.delete()


async def cancel(
        message: types.Message,
        state: FSMContext,
):
    """Отмена текущего действия"""
    await state.clear()
    await message.answer('Действие отменено', reply_markup=get_menu_keyboard())


common_handlers = Router()

common_handlers.message.register(start_handler, Command(commands=MyCommand.START))
common_handlers.callback_query.register(close_menu, CloseCallback.filter())
common_handlers.message.register(cancel, Command(commands=MyCommand.CANCEL))
