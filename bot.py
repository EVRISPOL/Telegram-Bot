from smc import detect_smc_signals
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from ohlc import fetch_ochl
def analyze_crypto(symbol="BTC/USDT", timeframe="3m"):
    try:
        df = fetch_ohlc(symbol, timeframe, 100)
        signals = detect_smc_signals(df)

        message = f"SMC Ανάλυση για {symbol} ({timeframe}):\n"
            for key, entries in signals.items():
            message += f"{key}: {entries}\n"

        return message
    except Exception as e:
        return f"Σφάλμα κατά την ανάλυση του {symbol}: {str(e)}"

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Γεια σου, είμαι έτοιμος!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Δοκίμασε άλλη εντολή!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("xrp", smc_handler))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
async def smc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = analyze_crypto(symbol="BTC/USDT", timeframe="3m")
    await update.message.reply_text(message)

app.run_polling()
async def smc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = "XRP/USDT"
        timeframe = "3m"
        analysis = analyze_crypto(symbol, timeframe)
        await update.message.reply_text(analysis)
    except Exception as e:
        await update.message.reply_text(f"Σφάλμα στην ανάλυση: {str(e)}")

