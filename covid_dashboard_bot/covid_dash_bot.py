import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import time
from chatbot import ChatBot

chatbot = ChatBot()

AUTH_TOKEN = '1170240889:AAHMoQb2mfowo4E9iIZjjXo4kHglo1dqz3c'
telegram_bot = telegram.Bot(token=AUTH_TOKEN)

updater = Updater(token=AUTH_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a Telegram Bot for the Integrated COVID-19 Dashboard. Ask me any queries about the website or about COVID-19.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def reply_to(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=chatbot.reply(update.message.text))

reply_handler = MessageHandler(Filters.text & (~Filters.command), reply_to)
dispatcher.add_handler(reply_handler)

updater.start_polling()
