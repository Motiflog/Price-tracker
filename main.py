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
GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# PRICE FETCHERS
# =========================
def get_gold_price():
    if not GOLDAPI_KEY:
        return None, None, None

    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLDAPI_KEY}

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()

    return data["price"], data["ch"], data["chp"]

def get_silver_price():
    if not GOLDAPI_KEY:
        return None, None, None

    url = "https://www.goldapi.io/api/XAG/USD"
    headers = {"x-access-token": GOLDAPI_KEY}

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()

    return data["price"], data["ch"], data["chp"]


# =========================
# COMMAND HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n"
        "I track US gold & silver prices.\n\n"
        "Commands:\n"
        "/gold – Current gold price\n"
        "/silver – Current silver price"
    )


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
# DAILY ALERT (GOLD + SILVER)
# =========================
async def daily_metals_alert(context: ContextTypes.DEFAULT_TYPE):
    gold_price, gold_ch, gold_chp = get_gold_price()
    silver_price, silver_ch, silver_chp = get_silver_price()

    if gold_price is None or silver_price is None:
        return

    msg = (
        "⏰ Daily Metals Update\n\n"
        f"🟡 Gold\n"
        f"💰 ${gold_price}\n"
        f"↕️ {gold_ch} ({gold_chp}%)\n\n"
        f"⚪ Silver\n"
        f"💰 ${silver_price}\n"
        f"↕️ {silver_ch} ({silver_chp}%)"
    )

    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

# =========================
# APP SETUP
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(CommandHandler("silver", silver))

    # Daily alert at 9 AM IST
    app.job_queue.run_daily(
        daily_metals_alert,
        time=time(hour=9, minute=0, tzinfo=pytz.timezone("Asia/Kolkata")),
    )

    app.run_polling()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
