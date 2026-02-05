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
        url = "https://api.metals.live/v1/spot"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            update.message.reply_text("⚠️ Price service unavailable.")
            return

        data = r.json()

        # data example: [["gold", 2034.5], ["silver", 22.8]]
        gold_price = None
        for item in data:
            if item[0] == "gold":
                gold_price = item[1]
                break

        if gold_price is None:
            update.message.reply_text("⚠️ Gold price not found.")
            return

        update.message.reply_text(
            f"🟡 Gold Price (US Spot)\n💵 ${gold_price}"
        )

    except Exception as e:
        update.message.reply_text(f"❌ Error:\n{e}")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("price", price))

updater.start_polling()
updater.idle()
