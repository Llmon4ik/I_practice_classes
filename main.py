import random
import sqlite3
import telebot
import config
import json
from datetime import datetime

conn = sqlite3.connect("DBBot.db", check_same_thread=False)
cursor = conn.cursor()
print('Бд подключена!')

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "test":
        bot.send_message(message.chat.id, "Hi!")

bot.infinity_polling()
