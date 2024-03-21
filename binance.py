"""My_BinanceBot on Telegram."""
import logging, os, io, datetime, pandas as pd
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from binance import Client
from telegram import Update, ForceReply
from telegram.ext import CallbackContext, CommandHandler, ApplicationBuilder
from dotenv import load_dotenv

load_dotenv()

T_API_KEY = os.getenv('T_API')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Help!')

async def get_btc_usdt(update: Update, context: CallbackContext) -> None:
    api_key = os.getenv('B_API')
    api_secret = os.getenv('SECRET')
    client = Client(api_key, api_secret)

    # Manage date format
    def unix_to_datetime(unix_time):
        return datetime.datetime.fromtimestamp(unix_time / 1000.0)
    
    def date_to_unix(date):
        date = datetime.datetime.now()
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date = date - datetime.timedelta(days=7)
        return int(date.timestamp()  * 1000)
    
    crypto = 'BTCUSDT'

    # Retrieve price data from api and plot against time
    klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_5MINUTE, date_to_unix(datetime.datetime.now()))
    values = [[unix_to_datetime(el[0]), float(el[1])] for el in klines]
    df = pd.DataFrame(values, columns=['ds', 'y'])
    plt.plot(df['ds'], df['y'])
    plt.xticks(rotation=15)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    await update.message.reply_photo(img)

def main() -> None:
    application = ApplicationBuilder().token(T_API_KEY).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    btc_usdt_handler = CommandHandler('btc', get_btc_usdt)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(btc_usdt_handler)
    
    application.run_polling()

if __name__=="__main__":
    main()