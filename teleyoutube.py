import os
import telebot
import re 
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.environ.get("TOKEN"))
out_path = 'out.mp3'
log_path = 'logs/my.log'

@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, "Welcome to the Telegram Youtube2MP3 Bot, just send a video link and I will send the mp3")

@bot.message_handler()
def handle_urls(message: telebot.types.Message):
    pattern = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
    if re.match(pattern, message.text):
        bot.reply_to(message, "Song is being downloaded, please wait")
        prompt = "yt-dlp -4 -o 'out.%(ext)s' --extract-audio --audio-format mp3 {} --rm-cache-dir".format(message.text)
        print(prompt)
        os.system(prompt)
        if os.path.isfile(out_path):
            audio = open(out_path, 'rb')
            bot.send_audio(chat_id=message.chat.id, audio=audio)
            os.remove(out_path)
        else:
            error_message = "Something went wrong"
            if os.path.isfile(log_path):
                with open(log_path, 'r') as f:
                    log = f.read()
                    f.close()
                error_message += "\n"
                error_message += log
                
            bot.reply_to(message, error_message)
    else:
        bot.reply_to(message, "Please send a valid youtube url!")


print('---BOT started---')
bot.infinity_polling()
