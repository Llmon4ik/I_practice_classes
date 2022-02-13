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


class User:
    def __init__(self, id):
        cursor.execute("SELECT * FROM user WHERE ID = {}".format(id))
        data = cursor.fetchone()

        if data:
            self.id = data[0]
            self.name = data[1]
            self.money = data[2]
        else:
            self.id = id
            self.name = "Пользователь"
            self.money = 1000

            cursor.execute("INSERT INTO user VALUES({}, '{}', {})".format(self.id, self.name, self.money))
            conn.commit()

    def change_nick(self, nick):
        self.name = nick

        cursor.execute("UPDATE user SET name = '{}' WHERE ID = {}".format(self.name, self.id))
        conn.commit()


@bot.message_handler(content_types=['text'])
def send_text(message):
    user_data = User(id=message.from_user.id)

    if message.text.lower() == "test":
        bot.send_message(message.chat.id, "Hi! {}".format(user_data.name))

    elif message.text.lower().split()[0] == "никнейм":
        text = message.text.split()

        if len(text[1]) > 12 or len(text[1]) < 1:
            bot.send_message(message.chat.id, "{}, ваш ник не может быть больше 12 или меньше 1 символа!".format(user_data.name))
        else:
            user_data.change_nick(text[1])
            bot.send_message(message.chat.id, "{}, никнейм успешно установлен!".format(user_data.name))

bot.infinity_polling()
