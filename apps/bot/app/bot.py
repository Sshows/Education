from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from app.config import settings

BOT_COMMANDS = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="calc", description="Рассчитать шанс"),
    BotCommand(command="programs", description="Программы"),
    BotCommand(command="universities", description="Вузы"),
    BotCommand(command="deadlines", description="Дедлайны"),
    BotCommand(command="profile", description="Профиль"),
    BotCommand(command="ask", description="AI-консультант"),
    BotCommand(command="sources", description="Источники"),
    BotCommand(command="help", description="Помощь"),
]


def _runtime_token() -> str:
    return settings.telegram_bot_token or "0000000000:development-placeholder-token"


bot = Bot(token=_runtime_token())
dp = Dispatcher()


def web_app_button(text: str, path: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=settings.webapp_url(path)))


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [web_app_button("Рассчитать шанс", "/calculator")],
            [web_app_button("Подобрать вуз", "/universities")],
            [web_app_button("Программы", "/programs")],
            [web_app_button("Спросить AI", "/ai")],
            [web_app_button("Дедлайны", "/deadlines")],
        ]
    )


def single_webapp_keyboard(text: str, path: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[web_app_button(text, path)]])


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я помогу оценить шанс поступления на грант или платное обучение по ЕНТ. Расчёт не является официальной гарантией, но использует открытые источники и исторические данные.",
        reply_markup=start_keyboard(),
    )


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Команды: /start, /calc, /programs, /universities, /deadlines, /profile, /ask, /sources, /help.",
        reply_markup=single_webapp_keyboard("Открыть Mini App", "/"),
    )


@dp.message(Command("calc"))
async def cmd_calc(message: Message) -> None:
    await message.answer(
        "Открой калькулятор:",
        reply_markup=single_webapp_keyboard("Открыть калькулятор", "/calculator"),
    )


@dp.message(Command("programs"))
async def cmd_programs(message: Message) -> None:
    await message.answer(
        "Каталог программ:",
        reply_markup=single_webapp_keyboard("Открыть программы", "/programs"),
    )


@dp.message(Command("universities"))
async def cmd_universities(message: Message) -> None:
    await message.answer(
        "Каталог вузов:",
        reply_markup=single_webapp_keyboard("Открыть вузы", "/universities"),
    )


@dp.message(Command("deadlines"))
async def cmd_deadlines(message: Message) -> None:
    await message.answer(
        "Дедлайны и правила поступления:",
        reply_markup=single_webapp_keyboard("Открыть дедлайны", "/deadlines"),
    )


@dp.message(Command("profile"))
async def cmd_profile(message: Message) -> None:
    await message.answer(
        "Профиль и история расчётов:",
        reply_markup=single_webapp_keyboard("Открыть профиль", "/profile"),
    )


@dp.message(Command("ask"))
async def cmd_ask(message: Message) -> None:
    await message.answer(
        "AI-консультант отвечает по подтверждённым источникам.",
        reply_markup=single_webapp_keyboard("Открыть AI-консультанта", "/ai"),
    )


@dp.message(Command("sources"))
async def cmd_sources(message: Message) -> None:
    await message.answer(
        "Открытые источники и статусы обновления:",
        reply_markup=single_webapp_keyboard("Источники данных", "/sources"),
    )
