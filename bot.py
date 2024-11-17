from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask setup
app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('BOTSTOKEN')  # Ensure you have set this in your environment variables

# Create the Telegram application
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Command handler to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! I am your echo bot.')

# Echo handler
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

# Add handlers to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def webhook():
    """Receive updates from Telegram as POST requests."""
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return 'OK'

@app.route('/')
def index():
    """A basic index route to check if the app is running."""
    return 'Telegram Echo Bot is running!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

