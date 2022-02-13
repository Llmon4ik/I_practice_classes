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
            self.rank = data[3]
        else:
            self.id = id
            self.name = "Пользователь"
            self.money = 1000
            self.rank = "user"

            cursor.execute("INSERT INTO user VALUES({}, '{}', {}, '{}')".format(self.id, self.name, self.money, self.rank))
            conn.commit()

    def change_nick(self, nick):
        self.name = nick

        cursor.execute("UPDATE user SET name = '{}' WHERE ID = {}".format(self.name, self.id))
        conn.commit()

    def change_rank(self, rank):
        self.rank = rank

        cursor.execute("UPDATE user SET rank = '{}' WHERE ID = {}".format(self.rank, self.id))
        conn.commit()

    def __repr__(self):
        return """ID: {}
Ник: {}
Деньги: {}
Ранг: {}
""".format(self.id, self.name, self.money, self.rank)

@bot.message_handler(content_types=['text'])
def send_text(message):
    user_data = User(id=message.from_user.id)

    if message.text.lower() == "test":
        bot.send_message(message.chat.id, "1")

    elif message.text.lower().split()[0] == "никнейм":
        text = message.text.split()

        if len(text) >= 2:
            if len(text[1]) <= 12 or len(text[1]) >= 1:
                user_data.change_nick(text[1])
                bot.send_message(message.chat.id, "{}, никнейм успешно установлен!".format(user_data.name))
            else:
                bot.send_message(message.chat.id, "{}, ваш ник не может быть больше 12 или меньше 1 символа!".format(user_data.name))

        else:
            bot.send_message(message.chat.id, "{}, Вы не указали ник!".format(user_data.name))

    # super-command

    if user_data.rank in ["develop", "admin", "moderator"]:
        if message.text.lower().split()[0] == "rank":
            bot.send_message(message.chat.id, "{}, Вы: {}".format(user_data.name, user_data.rank))

        elif message.text.lower().split()[0] == "get":
            text = message.text.lower().split()
            user_id = None

            if len(text) >= 2:
                if text[1].isdigit():
                    user_id = int(text[1])
            else:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id

            if user_id:
                userAnother_data = User(id=user_id)

                bot.send_message(message.chat.id, "Информация о пользователе:\n{}".format(userAnother_data))

    if user_data.rank in ["develop", "admin"]:
        pass

    if user_data.rank in ["develop"]:
        if message.text.lower().split()[0] == "give":
            text = message.text.lower().split()

            if len(text) > 1:
                if text[1] in ["admin", "moderator", "user"]:
                    user_id = None

                    if len(text) >= 3:
                        user_id = int(text[2])
                    else:
                        if message.reply_to_message:
                            user_id = message.reply_to_message.from_user.id

                    if user_id:
                        userAnother_data = User(id=user_id)
                        userAnother_data.change_rank(text[1])

                        bot.send_message(message.chat.id, "{}, Вы установили ранг: {}, пользователю: {}".format(user_data.name, text[1], userAnother_data.id))


        elif message.text.lower().split()[0] == "event":
            bot.send_message(message.chat.id, str(message))




bot.infinity_polling()
