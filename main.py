import os
import requests
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get("BOT_TOKEN")

def get_gold_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=XAUUSD=X"
    data = requests.get(url).json()
    return data["quoteResponse"]["result"][0]["regularMarketPrice"]

def start(update, context):
    update.message.reply_text(
        "👋 Welcome!\n"
        "I track US gold price.\n\n"
        "Commands:\n"
        "/price - Current gold price"
    )

def price(update, context):
    price = get_gold_price()
    update.message.reply_text(f"🟡 Gold Price (US): ${price}")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("price", price))

updater.start_polling()
updater.idle()
