"""
Telegram bot handlers and keyboard definitions.
No token is ever logged or hardcoded. TELEGRAM_BOT_TOKEN comes only from env.
"""
from __future__ import annotations

import re

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from app.config import settings

BOT_COMMANDS = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="calc", description="Рассчитать шанс на грант"),
    BotCommand(command="programs", description="Каталог программ ЕНТ"),
    BotCommand(command="universities", description="Вузы Казахстана"),
    BotCommand(command="deadlines", description="Дедлайны поступления"),
    BotCommand(command="profile", description="Мой профиль и история"),
    BotCommand(command="ask", description="AI-консультант"),
    BotCommand(command="sources", description="Источники данных"),
    BotCommand(command="help", description="Помощь"),
]

# Alias -> canonical pair key (mirrors ent_subjects.py)
_ALIAS_PAIRS: dict[str, tuple[str, str]] = {
    "физмат": ("mathematics", "physics"),
    "матфиз": ("mathematics", "physics"),
    "инфомат": ("mathematics", "informatics"),
    "матинф": ("mathematics", "informatics"),
    "химбио": ("biology", "chemistry"),
    "биохим": ("biology", "chemistry"),
    "биогео": ("biology", "geography"),
    "матгео": ("mathematics", "geography"),
    "химфиз": ("chemistry", "physics"),
    "истправо": ("world_history", "fundamentals_of_law"),
    "истгео": ("world_history", "geography"),
    "геоангл": ("geography", "foreign_language"),
    "казлит": ("kazakh_language", "kazakh_literature"),
    "руслит": ("russian_language", "russian_literature"),
}


def _runtime_token() -> str:
    return settings.telegram_bot_token or "0000000000:development-placeholder-token"


bot = Bot(token=_runtime_token())
dp = Dispatcher()


def _wa_button(text: str, path: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=settings.webapp_url(path)))


def _url_button(text: str, url: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, url=url)


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [_wa_button("🎯 Рассчитать шанс на грант", "/calculator")],
            [_wa_button("🏛 Подобрать вуз", "/universities"), _wa_button("📋 Программы", "/programs")],
            [_wa_button("🤖 AI-консультант", "/ai"), _wa_button("📅 Дедлайны", "/deadlines")],
        ]
    )


def single_webapp_keyboard(text: str, path: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[_wa_button(text, path)]])


def score_keyboard(score: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[_wa_button(f"🎯 Рассчитать с баллом {score}", f"/calculator?score={score}")]]
    )


def combo_keyboard(pair_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[_wa_button("📋 Посмотреть программы для этой комбинации", f"/programs?combo={pair_key}")]]
    )


# -------- Command handlers --------

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Deep link support: /start calc, /start programs, /start universities, /start ref_<id>
    args = message.text.split(maxsplit=1)[1] if message.text and " " in message.text else ""

    if args in ("calc", "calculator"):
        await message.answer("Открой калькулятор ЕНТ:", reply_markup=single_webapp_keyboard("🎯 Калькулятор", "/calculator"))
        return
    if args == "programs":
        await message.answer("Каталог программ:", reply_markup=single_webapp_keyboard("📋 Программы", "/programs"))
        return
    if args == "universities":
        await message.answer("Каталог вузов:", reply_markup=single_webapp_keyboard("🏛 Вузы", "/universities"))
        return

    name = message.from_user.first_name if message.from_user else "абитуриент"
    await message.answer(
        f"Привет, {name}! 👋\n\n"
        "Я помогу оценить *шанс поступления на грант* по результатам ЕНТ.\n\n"
        "Расчёт использует открытые источники и исторические данные — "
        "это ориентир, не гарантия.\n\n"
        "Выбери действие:",
        reply_markup=start_keyboard(),
        parse_mode="Markdown",
    )


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "📌 *Что умеет этот бот:*\n\n"
        "• `/calc` — калькулятор шанса на грант по баллу ЕНТ\n"
        "• `/programs` — список программ с предметными парами\n"
        "• `/universities` — каталог вузов Казахстана\n"
        "• `/deadlines` — срок подачи заявлений\n"
        "• `/ask` — AI-консультант по поступлению\n"
        "• `/sources` — открытые источники данных\n"
        "• `/profile` — история ваших расчётов\n\n"
        "💡 Просто отправьте _балл ЕНТ_ (0–140) или _комбинацию_ (физмат, инфомат, химбио…)",
        parse_mode="Markdown",
        reply_markup=single_webapp_keyboard("Открыть Mini App", "/"),
    )


@dp.message(Command("calc"))
async def cmd_calc(message: Message) -> None:
    await message.answer(
        "🎯 Открой калькулятор, выбери предметы и программу:",
        reply_markup=single_webapp_keyboard("Открыть калькулятор", "/calculator"),
    )


@dp.message(Command("programs"))
async def cmd_programs(message: Message) -> None:
    await message.answer("📋 Каталог программ:", reply_markup=single_webapp_keyboard("Открыть программы", "/programs"))


@dp.message(Command("universities"))
async def cmd_universities(message: Message) -> None:
    await message.answer("🏛 Каталог вузов:", reply_markup=single_webapp_keyboard("Открыть вузы", "/universities"))


@dp.message(Command("deadlines"))
async def cmd_deadlines(message: Message) -> None:
    await message.answer(
        "📅 Дедлайны и правила поступления:",
        reply_markup=single_webapp_keyboard("Открыть дедлайны", "/deadlines"),
    )


@dp.message(Command("profile"))
async def cmd_profile(message: Message) -> None:
    await message.answer("👤 Профиль и история расчётов:", reply_markup=single_webapp_keyboard("Открыть профиль", "/profile"))


@dp.message(Command("ask"))
async def cmd_ask(message: Message) -> None:
    await message.answer(
        "🤖 AI-консультант отвечает только с источниками и осторожными формулировками.",
        reply_markup=single_webapp_keyboard("Открыть AI-консультанта", "/ai"),
    )


@dp.message(Command("sources"))
async def cmd_sources(message: Message) -> None:
    await message.answer(
        "📊 Открытые источники данных (НЦТ, МНВО, приёмные комиссии):",
        reply_markup=single_webapp_keyboard("Источники данных", "/sources"),
    )


# -------- Smart text handler --------

_SCORE_RE = re.compile(r"^\s*(\d{1,3})\s*$")
_COMBO_RE = re.compile("|".join(re.escape(k) for k in _ALIAS_PAIRS), re.IGNORECASE)


@dp.message(F.text)
async def handle_text(message: Message) -> None:
    text = (message.text or "").strip()

    # 1. Detect raw ENT score
    score_match = _SCORE_RE.match(text)
    if score_match:
        score = int(score_match.group(1))
        if 0 <= score <= 140:
            await message.answer(
                f"🔢 Похоже, это ваш балл ЕНТ: *{score}*.\n\n"
                "Откройте калькулятор, выберите предметы, вуз и программу — "
                "и я покажу ориентировочный шанс на грант.",
                reply_markup=score_keyboard(score),
                parse_mode="Markdown",
            )
            return

    # 2. Detect subject combo alias
    combo_match = _COMBO_RE.search(text.lower())
    if combo_match:
        alias = combo_match.group(0).lower()
        subjects = _ALIAS_PAIRS[alias]
        pair_key = "+".join(sorted(subjects))
        label_map = {
            "физмат": "Математика + Физика",
            "матфиз": "Математика + Физика",
            "инфомат": "Математика + Информатика",
            "матинф": "Математика + Информатика",
            "химбио": "Биология + Химия",
            "биохим": "Биология + Химия",
            "биогео": "Биология + География",
            "матгео": "Математика + География",
            "химфиз": "Химия + Физика",
            "истправо": "Всемирная история + Основы права",
            "истгео": "Всемирная история + География",
            "геоангл": "География + Иностранный язык",
            "казлит": "Казахский язык + Литература",
            "руслит": "Русский язык + Литература",
        }
        label = label_map.get(alias, alias)
        await message.answer(
            f"📚 Распознана комбинация предметов: *{label}*\n\n"
            "Посмотрите программы, доступные по этой комбинации:",
            reply_markup=combo_keyboard(pair_key),
            parse_mode="Markdown",
        )
        return

    # 3. Default: redirect to Mini App
    await message.answer(
        "Не понял запрос 🤔\n\n"
        "Отправь *балл ЕНТ* (например: 87) или *комбинацию предметов* (физмат, инфомат, химбио…)\n"
        "Или открой Mini App для полного расчёта:",
        reply_markup=single_webapp_keyboard("🎯 Открыть калькулятор", "/calculator"),
        parse_mode="Markdown",
    )
