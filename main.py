import os
import requests
from datetime import time
import pytz

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
METALS_API_KEY = os.getenv("METALS_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# PRICE FETCHERS
# =========================
def get_gold_price():
    if not METALS_API_KEY:
        return None, None, None

    url = "https://api.metals.live/v1/spot/gold"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()[0]

    return data["price"], data["ch"], data["chp"]


def get_silver_price():
    if not METALS_API_KEY:
        return None, None, None

    url = "https://api.metals.live/v1/spot/silver"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()[0]

    return data["price"], data["ch"], data["chp"]

# =========================
# COMMAND HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n"
        "I track US gold & silver prices.\n\n"
        "Commands:\n"
        "/price – Gold price\n h"
        "/silver – Silver price"
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, ch, chp = get_gold_price()
    if price is None:
        await update.message.reply_text("❌ API key not set.")
        return

    await update.message.reply_text(
        f"🟡 Gold Price (US)\n"
        f"💰 ${price}\n"
        f"↕️ 24h Change: {ch} ({chp}%)"
    )


async def silver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, ch, chp = get_silver_price()
    if price is None:
        await update.message.reply_text("❌ API key not set.")
        return

    await update.message.reply_text(
        f"⚪ Silver Price (US)\n"
        f"💰 ${price}\n"
        f"↕️ 24h Change: {ch} ({chp}%)"
    )

# =========================
# DAILY ALERT JOB
# =========================
async def daily_gold_alert(context: ContextTypes.DEFAULT_TYPE):
    price, ch, chp = get_gold_price()
    if price is None:
        return

    msg = (
        "⏰ Daily Gold Update\n"
        f"💰 ${price}\n"
        f"↕️ 24h Change: {ch} ({chp}%)"
    )

    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

# =========================
# APP SETUP
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("silver", silver))

    # Daily alert at 9 AM IST
    app.job_queue.run_daily(
        daily_gold_alert,
        time=time(hour=9, minute=0, tzinfo=pytz.timezone("Asia/Kolkata")),
    )

    app.run_polling()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
