
def get_silver_price():
    api_key = os.getenv("GOLDAPI_KEY")
    if not api_key:
        return None, None, None

    url = "https://www.goldapi.io/api/XAG/USD"
    headers = {"x-access-token": api_key}

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()

    return data["price"], data["ch"], data["chp"]import os
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
 def silver(update, context):
    price, change, change_pct = get_silver_price()

    if price is None:
        update.message.reply_text("❌ API key not set.")
        return

    msg = (
        "🥈 Silver Price (US)\n"
        f"💲 {price}\n"
        f"↕️ 24h Change: {change} ({change_pct}%)"
    )

    update.message.reply_text(msg)

def price(update, context):
    try:
        api_key = os.environ.get("GOLDAPI_KEY")
        if not api_key:
            update.message.reply_text("❌ API key not set.")
            return

        url = "https://www.goldapi.io/api/XAU/USD"
        headers = {
            "x-access-token": api_key,
            "Content-Type": "application/json"
        }

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            update.message.reply_text("⚠️ Price service unavailable.")
            return

        data = r.json()

        price = data.get("price")
        change = data.get("ch")
        change_pct = data.get("chp")

        msg = (
            f"🟡 Gold Price (US)\n"
            f"💵 ${price}\n"
            f"📉 24h Change: {change} ({change_pct}%)"
        )

        update.message.reply_text(msg)

    except Exception as e:
        update.message.reply_text(f"❌ Error:\n{e}")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("price", price))
dp.add_handler(CommandHandler("silver", silver))

def daily_gold_alert(context):
    price, change, change_pct = get_gold_price()
    if price is None:
        return

    msg = (
        "⏰ Daily Gold Update\n"
        f"💰 ${price}\n"
        f"↕️ 24h Change: {change} ({change_pct}%)"
    )

    context.bot.send_message(chat_id=YOUR_CHAT_ID, text=msg)

updater.start_polling()
updater.idle()
