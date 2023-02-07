import os
import telebot
import re 
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.environ.get("TOKEN"))

@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, "Welcome to the Telegram Youtube2MP3 Bot, just send a video link and I will send the mp3")

@bot.message_handler()
def handle_urls(message: telebot.types.Message):
    pattern = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
    if re.match(pattern, message.text):
        bot.reply_to(message, "Song is being downloaded, please wait")
        prompt = "youtube-dl -4 -o 'out.%(ext)s' --extract-audio --audio-format mp3 {} --rm-cache-dir".format(message.text)
        print(prompt)
        os.system(prompt)
        audio = open('out.mp3', 'rb')
        bot.send_audio(chat_id=message.chat.id, audio=audio)

    else:
        bot.reply_to(message, "Please send a valid youtube url!")


print('---BOT started---')
bot.infinity_polling()