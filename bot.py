"""Telegram bot for TON and RUB conversion."""

from __future__ import annotations

import asyncio
import logging
import os
import re
from decimal import Decimal

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from converter import (
    CACHE_TTL,
    RATE_CACHE,
    convert_rub_to_ton,
    convert_ton_to_rub,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BROADCAST_CHAT_ID = os.getenv("BROADCAST_CHAT_ID")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

RATE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=toncoin&vs_currencies=rub"

# Regex patterns for message parsing
PATTERN_TON = re.compile(r"^(\d+[\.,]?\d*)\s*ton$", re.IGNORECASE)
PATTERN_RUB = re.compile(r"^(\d+[\.,]?\d*)\s*rub$", re.IGNORECASE)


def get_rate() -> Decimal:
    """Fetch TON price in RUB with simple caching."""
    from time import time

    cached = RATE_CACHE.get("rate")
    now = time()
    if cached and now - cached[1] < CACHE_TTL:
        return cached[0]

    response = requests.get(RATE_URL, timeout=10)
    data = response.json()
    rate = Decimal(str(data["toncoin"]["rub"]))
    RATE_CACHE["rate"] = (rate, now)
    return rate


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a short help message."""
    await update.message.reply_text(
        "Отправьте сообщение вида `50 ton` или `1000 rub`, и я пришлю результат."
    )


async def convert_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle plain text conversion requests."""
    text = update.message.text.strip()

    match = PATTERN_TON.match(text)
    if match:
        amount = Decimal(match.group(1).replace(",", "."))
        rate = get_rate()
        result = convert_ton_to_rub(amount, rate)
        await update.message.reply_text(f"≈ {result} ₽")
        return

    match = PATTERN_RUB.match(text)
    if match:
        amount = Decimal(match.group(1).replace(",", "."))
        rate = get_rate()
        result = convert_rub_to_ton(amount, rate)
        await update.message.reply_text(f"≈ {result} TON")
        return

    await update.message.reply_text(
        "Не понимаю. Отправьте, например, `1.5 ton` или `2000 rub`."
    )


async def broadcast_rate(application: Application) -> None:
    """Periodically broadcast the current rate to a chat."""
    if not BROADCAST_CHAT_ID:
        return

    while True:
        rate = get_rate()
        await application.bot.send_message(
            BROADCAST_CHAT_ID, f"1 TON = {rate} ₽"
        )
        await asyncio.sleep(900)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, convert_message)
    )

    if BROADCAST_CHAT_ID:
        application.job_queue.run_repeating(
            lambda _: application.bot.send_message(
                BROADCAST_CHAT_ID, f"1 TON = {get_rate()} ₽"
            ),
            interval=900,
            first=0,
        )

    application.run_polling()


if __name__ == "__main__":
    main()
