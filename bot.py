from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging

# Define your bot token (Replace with your actual token)
TELEGRAM_API_TOKEN = os.getenv('BOTSTOKEN')
#WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Initialize Flask
app = Flask(__name__)

# Define the Telegram Bot handler functions
def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text('Hello! Send me anything, and I will echo it back!')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user's message."""
    update.message.reply_text(update.message.text)

# Flask route for the webhook
@app.route('/' + TELEGRAM_API_TOKEN, methods=['POST'])
#def webhook():
#    """Handle webhook requests from Telegram."""
#    json_str = request.get_json(force=True)
#    update = Update.de_json(json_str, updater.bot)
#    updater.dispatcher.process_update(update)
#    return 'ok'

def main():
    """Start the Flask app and set webhook."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Set webhook
    updater.bot.setWebhook(WEBHOOK_URL + TELEGRAM_API_TOKEN)

    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()

