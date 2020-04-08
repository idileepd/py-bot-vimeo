import time
import telebot
import os
import sys
TOKEN = "1148821460:AAGfLhk0rKp5SPzTCwcgWJ2tYQngDBms1H4"
bot = telebot.TeleBot(token=TOKEN)
# bot = telebot.AsyncTeleBot(token=TOKEN)
print("ASYNC Bot Started :)")


@bot.message_handler(commands=['start'])  # welcome message handler
def send_welcome(message):
    time.sleep(10)
    bot.reply_to(message, 'hii welcome!!!')




@bot.message_handler(commands=['help'])  # help message handler
def send_help(message):

    bot.reply_to(
        message, '/d - cmd to download vimeo file with name \n Ex: /d fileName@http://vimep..json\n/dd - cmd to direct download file\n\n/help - help cmd')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        exit()
        
