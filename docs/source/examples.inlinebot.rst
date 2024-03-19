import logging
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, Job

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        2: [MessageHandler(Filters.text & ~Filters.command, get_favorite_color)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask for the user's name."""
    update.message.reply_text('Hello! What is your name?')
    return 1

def get_name(update: Update, context: CallbackContext) -> int:
    """Save the user's name and ask for their favorite color."""
    user_name = update.message.text
    context.user_data['name'] = user_name
    update.message.reply_text(f'Nice to meet you, {user_name}! What is your favorite color?')
    return 2

def get_favorite_color(update: Update, context: CallbackContext) -> int:
    """
