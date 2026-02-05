import os
import requests
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get("BOT_TOKEN")

def get_gold_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=XAUUSD=X"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()
    return data["quoteResponse"]["result"][0]["regularMarketPrice"]

def start(update, context):
    update.message.reply_text(
        "👋 Welcome!\n"
        "I track US gold price.\n\n"
        "Commands:\n"
        "/price - Current gold price"
    )

def price(update, context):
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=XAUUSD=X"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            update.message.reply_text("⚠️ Yahoo blocked the request.")
            return

        data = r.json()

        if "quoteResponse" not in data:
            update.message.reply_text(
                "⚠️ Yahoo response format changed.\nTry again later."
            )
            return

        result = data["quoteResponse"].get("result", [])

        if not result:
            update.message.reply_text("⚠️ Gold price not available.")
            return

        price = result[0].get("regularMarketPrice")

        if price is None:
            update.message.reply_text("⚠️ Price missing in response.")
            return

        update.message.reply_text(f"🟡 Gold Price (US): ${price}")

    except Exception as e:
        update.message.reply_text(f"❌ Error:\n{e}")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("price", price))

updater.start_polling()
updater.idle()
