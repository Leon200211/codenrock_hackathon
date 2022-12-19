import telebot
import random
from telebot import types # для указание типов
from collections import defaultdict
import requests
import base64
from io import StringIO


# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

messages = ['', '']  # для отлова ролей
admin_state = [0, '']  # для админа
trend = ['', '']


# Команда start
@bot.message_handler(commands=["start"])
def start(message):


    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для вывода новостей!".format(
                         message.from_user))





@bot.message_handler(content_types=['audio'])
def photo(message):
    fileID = message.audio.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.wav", 'wb') as new_file:
        new_file.write(downloaded_file)



    with open('image.wav', 'r', encoding='unicode_escape') as f:

        print(f)

        stream = StringIO(f.read())
        file = base64.b64encode(stream.getvalue().encode())

        res = requests.post('http://projectvoid.play.ai/audio-to-table/', data={'wav':file, 'coded':'base64'})

        print(res.content)

        my_bytes = base64.b64decode(res.content)

    with open("my_file.csv", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(my_bytes)



    with open("my_file.csv", "rb") as csv:

        bot.send_document(message.chat.id, csv)



# Запускаем бота
bot.polling(none_stop=True, interval=0)
