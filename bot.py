import time
import telebot
import os
import sys
import drive_api as drive
import vimeo_api as vimeo
from flask import Flask, request
import shutil


TOKEN = "1148821460:AAGfLhk0rKp5SPzTCwcgWJ2tYQngDBms1H4"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

default_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'
current_set_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'

grp_Chat_id = '-478269081'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

heroku_web_url = 'https://py-bot-vimeo.herokuapp.com/'

#removing output and temp files
print("\n\n Removing Output directory and Temp directory")
if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
    print('removing output directory')
    shutil.rmtree(OUTPUT_DIR)

if os.path.exists(TEMP_DIR) and os.path.isdir(TEMP_DIR):
    print('removing temp directory')
    shutil.rmtree(TEMP_DIR)

print("##################################################################################")
print('Bot Started :)')
print("##################################################################################")
print("##################################################################################")
print("##################################################################################")

@bot.message_handler(commands=['start'])  # welcome message handler
def send_welcome(message):
    print(f"\n\n Start MEssage :: \n{message}\n\n")
    bot.reply_to(message, 'hii welcome!!!')

@bot.message_handler(commands=['help'])  # help message handler
def send_help(message):
    bot.reply_to(
        message, '/d - cmd to download vimeo file with name \n Ex: /d fileName@http://vimep..json\n/dd - cmd to direct download file\n\n/current_dir - get current google drive directory \n\n/reset_dir - reset google  drive downlaod directory to defult \n\n/change_dir <<dir name>> - change the current directory to your specified directory')

#/--------------------------------------------------- BOTTTT---------------------------------------
@bot.message_handler(commands=['change_dir'])  # help message handler
def change_download_drive_dir(message):
    folder_id = message.text[11:]
    print(folder_id)
    print("ASSUMING Folder exist bro...")
    global current_set_dir
    current_set_dir = folder_id
    print("Current Set Dir ", current_set_dir)
    bot.reply_to(message, '\nCurrent Directory Id:\n'+current_set_dir)


@bot.message_handler(commands=['reset_dir'])  # help message handler
def reser_download_drive_dir(message):
    folder_id = message.text[11:]
    print(folder_id)
    global current_set_dir
    global default_dir
    current_set_dir = default_dir
    print("Reset to default directory", current_set_dir)
    bot.reply_to(message, '\nCurrent Directory Id:\n'+current_set_dir)




@bot.message_handler(commands=['current_dir'])  # help message handler
def current_download_drive_dir(message):
    print("Current Dir ", current_set_dir)
    bot.reply_to(message, '\nCurrent Directory Id:\n'+current_set_dir)



@bot.message_handler(commands=['d'])  # help message handler
def name_download(message):
    try:
        # bot.reply_to(message, 'download started...')
        fulltext = message.text[3:].split('@')
        if((fulltext[1] is None) or ('json' not in fulltext[1])):
            return bot.reply_to(message, "vimeo url err")
        if(fulltext[0] is None):
            return bot.reply_to(message, "filename err")

        download_request(fulltext[0], fulltext[1], message)
        
    except IndexError:
        bot.reply_to(message, "Please check command.")
        print(f"\n\n\n\n\n {fulltext} command error of /d")
    except:
        print(f"\n\n\n\n\n {fulltext} Something err in download_request() function.")
        bot.reply_to(message, "something went wrong")


def download_request(file_name, master_json_url, message):
    bot.reply_to(message, file_name+'::\n Download just started.')
    [download_status, download_message] = vimeo.vimeo_downloader(master_json_url, file_name, False, False)
    print(f"download status :: {download_status}")
    print(f"download message :: {download_message}")
    if(download_status == True):
        bot.reply_to(message, file_name+'\n::Download video part over. \n Now Uploading to GoogleDrive')
        #UPLOAD TO GDRIVE
        global current_set_dir
        print(f'uploading..  :: {file_name} to folder :: {current_set_dir}')
        [upload_status, upload_message]= drive.upload_video_to_this_folder(current_set_dir,download_message)
        print(f"upload status :: {upload_status}")
        print(f"upload message :: {upload_message}")
        if(upload_status == True):
            bot.reply_to(message, file_name+'\n::File Uploaded to drive Successfully')
        else:
            bot.reply_to(message, upload_message)
    else:
        bot.reply_to(message, download_message)
    return

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200

@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url=heroku_web_url + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))