"""
Telegram bot handlers and keyboard definitions.
No token is ever logged or hardcoded. TELEGRAM_BOT_TOKEN comes only from env.
"""
from __future__ import annotations

import re

import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Message, PreCheckoutQuery, WebAppInfo

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
    BotCommand(command="premium", description="Premium и оплата Stars"),
    BotCommand(command="buy", description="Купить полный прогноз"),
    BotCommand(command="payments", description="Мои платежи"),
    BotCommand(command="restore", description="Восстановить доступ"),
    BotCommand(command="support", description="Поддержка"),
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

PAYMENT_PRODUCTS = {
    "pro_once": {
        "title": "Полный прогноз",
        "description": "Расширенный прогноз, рекомендации, источники и сравнение score vs cutoff.",
        "stars_price": 50,
    },
    "ai_pack": {
        "title": "AI-пакет",
        "description": "20 вопросов AI-консультанту с ответами по источникам.",
        "stars_price": 100,
    },
    "premium_month": {
        "title": "Premium на месяц",
        "description": "Безлимитные прогнозы, 100 AI-вопросов, профиль и дедлайн-алерты.",
        "stars_price": 250,
    },
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
            [_wa_button("Premium", "/pricing"), InlineKeyboardButton(text="Купить полный прогноз", callback_data="buy:pro_once")],
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


def pricing_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Полный прогноз — 50 Stars", callback_data="buy:pro_once")],
            [InlineKeyboardButton(text="AI-пакет — 100 Stars", callback_data="buy:ai_pack")],
            [InlineKeyboardButton(text="Premium на месяц — 250 Stars", callback_data="buy:premium_month")],
            [_wa_button("Открыть страницу Premium", "/pricing")],
        ]
    )


def success_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [_wa_button("Открыть Mini App", "/")],
            [_wa_button("Открыть полный прогноз", "/result/demo")],
        ]
    )


async def _api_request(method: str, path: str, **kwargs):
    if not settings.api_url:
        raise RuntimeError("API_URL is not configured")
    base = settings.api_url.rstrip("/")
    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.request(method, f"{base}{path}", **kwargs)
        response.raise_for_status()
        return response.json()


async def create_stars_order(product_code: str, telegram_id: int | None) -> dict:
    return await _api_request(
        "POST",
        "/api/payments/telegram-stars/order",
        json={
            "product_code": product_code,
            "telegram_id": telegram_id,
            "idempotency_key": f"tg-stars:{telegram_id}:{product_code}",
            "metadata": {"source": "bot"},
        },
    )


async def get_order(order_id: int) -> dict:
    return await _api_request("GET", f"/api/payments/orders/{order_id}")


async def confirm_stars_payment(payment, telegram_id: int | None) -> dict:
    return await _api_request(
        "POST",
        "/api/payments/telegram-stars/confirm",
        json={
            "order_id": int(payment.invoice_payload),
            "telegram_id": telegram_id,
            "total_amount": payment.total_amount,
            "currency": payment.currency,
            "telegram_payment_charge_id": payment.telegram_payment_charge_id,
            "provider_payment_id": payment.provider_payment_charge_id,
            "raw_payload": {
                "invoice_payload": payment.invoice_payload,
                "telegram_payment_charge_id": payment.telegram_payment_charge_id,
                "provider_payment_charge_id": payment.provider_payment_charge_id,
            },
        },
    )


async def send_stars_invoice(message: Message, product_code: str) -> None:
    product = PAYMENT_PRODUCTS.get(product_code)
    if not product:
        await message.answer("Неизвестный продукт. Откройте /premium и выберите тариф ещё раз.")
        return
    try:
        order = await create_stars_order(product_code, message.from_user.id if message.from_user else None)
    except Exception:
        await message.answer("Не удалось создать заказ. Попробуйте позже или напишите /support.")
        return

    await bot.send_invoice(
        chat_id=message.chat.id,
        title=product["title"],
        description=product["description"],
        payload=str(order["order_id"]),
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=product["title"], amount=product["stars_price"])],
        start_parameter=f"buy_{product_code}",
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
    if args in ("pricing", "premium"):
        await message.answer("Premium доступ и Telegram Stars:", reply_markup=pricing_keyboard())
        return
    if args.startswith("buy_"):
        await send_stars_invoice(message, args.replace("buy_", "", 1))
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
        "• `/premium` — тарифы и Telegram Stars\n"
        "• `/payments` — статус платежей и доступа\n"
        "• `/restore` — восстановить доступ\n"
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


@dp.message(Command("premium"))
async def cmd_premium(message: Message) -> None:
    await message.answer(
        "Premium открывает полный прогноз, рекомендации, разбор источников и AI-лимиты.\n\n"
        "В Telegram для цифрового доступа используется Stars.",
        reply_markup=pricing_keyboard(),
    )


@dp.message(Command("buy"))
async def cmd_buy(message: Message) -> None:
    await message.answer("Выберите продукт для оплаты Stars:", reply_markup=pricing_keyboard())


@dp.message(Command("payments"))
async def cmd_payments(message: Message) -> None:
    await message.answer(
        "Статус платежей и доступов можно открыть в Mini App.",
        reply_markup=single_webapp_keyboard("Профиль и биллинг", "/profile/billing"),
    )


@dp.message(Command("restore"))
async def cmd_restore(message: Message) -> None:
    telegram_id = message.from_user.id if message.from_user else None
    try:
        entitlements = await _api_request("GET", "/api/payments/my-entitlements", params={"telegram_id": telegram_id})
    except Exception:
        await message.answer("Не удалось проверить доступ. Попробуйте позже или напишите /support.")
        return

    if not entitlements:
        await message.answer(
            "Активный Premium-доступ не найден. Если оплата прошла, но доступ не появился — напишите /support.",
            reply_markup=pricing_keyboard(),
        )
        return

    names = ", ".join(item["product_code"] for item in entitlements)
    await message.answer(f"Доступ восстановлен: {names}", reply_markup=success_keyboard())


@dp.message(Command("support"))
async def cmd_support(message: Message) -> None:
    contact = settings.support_telegram_username or settings.support_email or "укажите SUPPORT_TELEGRAM_USERNAME в Railway"
    await message.answer(
        "Если оплата прошла, но доступ не появился — нажмите /restore или напишите в поддержку.\n\n"
        f"Контакт: {contact}",
        reply_markup=single_webapp_keyboard("Открыть поддержку", "/support"),
    )


@dp.callback_query(F.data.startswith("buy:"))
async def cb_buy(callback: CallbackQuery) -> None:
    product_code = callback.data.split(":", 1)[1] if callback.data else ""
    if callback.message:
        await send_stars_invoice(callback.message, product_code)
    await callback.answer()


@dp.pre_checkout_query()
async def handle_pre_checkout(query: PreCheckoutQuery) -> None:
    try:
        order = await get_order(int(query.invoice_payload))
        expected_ok = (
            order["provider"] == "telegram_stars"
            and order["currency"] == "XTR"
            and int(order["amount"]) == int(query.total_amount)
            and query.currency == "XTR"
            and order["status"] in {"created", "pending"}
        )
    except Exception:
        expected_ok = False

    if expected_ok:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Заказ не найден или сумма изменилась. Создайте заказ заново.")


@dp.message(F.successful_payment)
async def handle_successful_payment(message: Message) -> None:
    payment = message.successful_payment
    if not payment:
        return
    try:
        await confirm_stars_payment(payment, message.from_user.id if message.from_user else None)
    except Exception:
        await message.answer(
            "Оплата получена, но доступ не активировался автоматически. Нажмите /restore или напишите /support.",
        )
        return

    await message.answer(
        "Оплата прошла. Premium активирован.\n\n"
        "Если доступ не появился — нажмите /restore или напишите /support.",
        reply_markup=success_keyboard(),
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
