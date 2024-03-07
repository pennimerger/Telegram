"""Score4me Telegram Bot."""
import logging, os, subprocess, scores
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv

load_dotenv()

livescores = scores.get_scores()
API_KEY = os.getenv('API_KEY')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello, check livescores with ease!")
    
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    script_path = "livescores.py"
    subprocess.call(["python", script_path])
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text = livescores
        )
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_KEY).build()
    
    start_handler = CommandHandler('start', start)
    score_handler = CommandHandler('score', score)
    application.add_handler(start_handler)
    application.add_handler(score_handler)
    
    application.run_polling()