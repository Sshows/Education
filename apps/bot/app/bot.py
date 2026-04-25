from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from app.config import settings

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть калькулятор", web_app=WebAppInfo(url=f"{settings.telegram_webapp_url}/calculator"))],
        [InlineKeyboardButton(text="Подобрать вуз", web_app=WebAppInfo(url=f"{settings.telegram_webapp_url}/universities"))],
        [InlineKeyboardButton(text="Спросить AI", web_app=WebAppInfo(url=f"{settings.telegram_webapp_url}/ai"))],
        [InlineKeyboardButton(text="Дедлайны", callback_data="deadlines")],
    ])


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я помогу оценить шанс поступления на грант или платное обучение по ЕНТ. Расчёт не является официальной гарантией, но использует открытые источники и исторические данные.",
        reply_markup=start_keyboard(),
    )


@dp.message(Command("calc"))
async def cmd_calc(message: Message):
    await message.answer("Открой калькулятор:", reply_markup=start_keyboard())


@dp.message(Command("profile"))
async def cmd_profile(message: Message):
    await message.answer("Профиль пользователя доступен в Mini App: /profile")


@dp.message(Command("universities"))
async def cmd_universities(message: Message):
    await message.answer("Каталог вузов: откройте Mini App /universities")


@dp.message(Command("programs"))
async def cmd_programs(message: Message):
    await message.answer("Каталог программ: откройте Mini App /programs")


@dp.message(Command("deadlines"))
async def cmd_deadlines(message: Message):
    await message.answer("Дедлайны уточняйте по testcenter.kz и gov.kz")


@dp.message(Command("ask"))
async def cmd_ask(message: Message):
    await message.answer("Задайте вопрос. Если данных нет: Подтверждённых данных в источниках нет.")


@dp.message(Command("sources"))
async def cmd_sources(message: Message):
    await message.answer("Источники: testcenter.kz, gov.kz, enic-kazakhstan.edu.kz, сайты вузов")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Команды: /start /calc /profile /universities /programs /deadlines /ask /sources /help")


@dp.callback_query(F.data == "deadlines")
async def cb_deadlines(cb):
    await cb.message.answer("Дедлайны уточняйте в НЦТ и МНВО. Источники: testcenter.kz, gov.kz")
    await cb.answer()
