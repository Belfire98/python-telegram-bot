import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

# 1. Telegram Bot Setup
from bot_manager import telegram_bot_manager

# 2. Web Framework Setup
app = Flask(__name__)

@app.route('/<token>', methods=['POST'])
def webhook(token):
    if token == os.environ['TELEGRAM_BOT_TOKEN']:
        update = Update.de_json(request.get_json(force=True), bot)
        telegram_bot_manager.process_new_updates([update])
        return ''
    else:
        return 'Invalid token'

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    url = f'https://{os.environ["WEBAPP_HOST"]}:{os.environ["PORT"]}/{os.environ["TELEGRAM_BOT_TOKEN"]}'
    s = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True).bot.set_webhook(url)
    if s:
        return jsonify({'status': 'Webhook set'})
    else:
        return jsonify({'status': 'Webhook not set'})

# 3. Main Application
if __name__ == '__main__':
    telegram_bot_manager.init_bot()
    app.run(host=os.environ['WEBAPP_HOST'], port=os.environ['PORT'])
