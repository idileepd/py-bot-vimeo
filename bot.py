import time
import telebot
import os
import sys
import drive_api as drive
import vimeo_api as vimeo
import shutil


TOKEN = "1256163582:AAEUbeS_KJ77AXv68zY13beIM03FoG0H7eg"
# bot = telebot.TeleBot(token=TOKEN)
bot = telebot.AsyncTeleBot(token=TOKEN)

default_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'
current_set_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'

grp_Chat_id = '-478269081'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

heroku_web_url = 'https://py-bot-vimeo.herokuapp.com/'

all_download_status = {}


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
    send_delete_clean_msg(message, 'welcome to glat to see you. \n what you will download today')

@bot.message_handler(commands=['shutdown'])  # welcome message handler
def exit_program(message):
    print("Exiting program")
    send_delete_clean_msg(message, 'shutting down bot')
    bot.stop_bot()
    quit()

@bot.message_handler(commands=['help'])  # help message handler
def send_help(message):
    send_delete_clean_msg(message, '/d - cmd to download vimeo file with name \n Ex: /d fileName@http://vimep..json\n/dd - cmd to direct download file\n\n/current_dir - get current google drive directory \n\n/reset_dir - reset google  drive downlaod directory to defult \n\n/change_dir <<dir name>> - change the current directory to your specified directory')

#/--------------------------------------------------- BOTTTT---------------------------------------
@bot.message_handler(commands=['change_dir'])  # help message handler
def change_download_drive_dir(message):
    folder_id = message.text[11:]
    print(folder_id)
    print("ASSUMING Folder exist bro...")
    global current_set_dir
    current_set_dir = folder_id
    print("Current Set Dir ", current_set_dir)
    send_delete_clean_msg(message, '\nCurrent Directory Id:\n'+current_set_dir)


@bot.message_handler(commands=['reset_dir'])  # help message handler
def reser_download_drive_dir(message):
    folder_id = message.text[11:]
    print(folder_id)
    global current_set_dir
    global default_dir
    current_set_dir = default_dir
    print("Reset to default directory", current_set_dir)
    send_delete_clean_msg(message, '\nCurrent Directory Id:\n'+current_set_dir)




@bot.message_handler(commands=['current_dir'])  # help message handler
def current_download_drive_dir(message):
    print("Current Dir ", current_set_dir)
    send_delete_clean_msg(message, '\nCurrent Directory Id:\n'+current_set_dir)

@bot.message_handler(commands=['status'])  # help message handler
def status_send(message):
    chat_id = get_chat_id(message)
    show_download_status(chat_id)

@bot.message_handler(commands=['status_clear'])  # help message handler
def clear_status(message):
    chat_id = get_chat_id(message)
    send_delete_clean_msg(message, 'status')

# @bot.message_handler(commands=['d'])  # help message handler
# def name_download(message):
    
#     try:
#         # bot.reply_to(message, 'download started...')
#         fulltext = message.text[3:].split('@')
#         if((fulltext[1] is None) or ('json' not in fulltext[1])):
#             return bot.reply_to(message, "vimeo url err")
#         if(fulltext[0] is None):
#             return bot.reply_to(message, "filename err")

#         global download_status
#         download_status[fulltext[0]] = {'name':fulltext[0], 'status':'got request'}
#         download_request(fulltext[0], fulltext[1], message)
        
#     except IndexError:
#         download_status[fulltext[0]]['status'] = 'download Error, check command'
#         bot.reply_to(message, "Please check command.")
#         print(f"\n\n\n\n\n {fulltext} command error of /d")
#     except:
#         download_status[fulltext[0]]['status'] = 'download Error, something wrong'
#         print(f"\n\n\n\n\n {fulltext} Something err in download_request() function.")
#         bot.reply_to(message, "something went wrong")
#     finally:
#         print(download_status)

   
@bot.message_handler(commands=['d'])  # help message handler
def name_download(message):
    # bot.reply_to(message, 'download started...')
    fulltext = message.text[3:].split('@')
    if((fulltext[1] is None) or ('json' not in fulltext[1])):
        return bot.reply_to(message, "vimeo url err")
    if(fulltext[0] is None):
        return bot.reply_to(message, "filename err")

    global download_status
    all_download_status[fulltext[0]] = {'name':fulltext[0], 'status':'got request'}
    download_request(fulltext[0], fulltext[1], message)


def download_request(file_name, master_json_url, message):
    global all_download_status
    send_delete_clean_msg(message, file_name+'::\n Download just started.')
    all_download_status[file_name]['status'] = 'download just started'
    [download_status, download_message] = vimeo.vimeo_downloader(master_json_url, file_name, False, False)
    print(f"download status :: {download_status}")
    print(f"download message :: {download_message}")
    if(download_status == True):
        all_download_status[file_name]['status'] = 'download part over'
        send_delete_clean_msg(message, file_name+'\n::Download video part over. \n Now Uploading to GoogleDrive')
        #UPLOAD TO GDRIVE
        global current_set_dir
        print(f'uploading..  :: {file_name} to folder :: {current_set_dir}')
        [upload_status, upload_message]= drive.upload_video_to_this_folder(current_set_dir,download_message)
        print(f"upload status :: {upload_status}")
        print(f"upload message :: {upload_message}")
        if(upload_status == True):
            all_download_status[file_name]['status'] = 'Success. file completed'
            send_delete_clean_msg(message, file_name+'\n::File Uploaded to drive Successfully')
        else:
            all_download_status[file_name]['status'] = 'Upload to drive failed'
            bot.reply_to(message, upload_message)
    else:
        all_download_status[file_name]['status'] = 'Download failed'
        bot.reply_to(message, download_message)
    print(f"\n\n Download Status\n\n{all_download_status}")
    return


def send_delete_clean_msg(message, msg):
    chat_id = get_chat_id(message)
    bot.send_message(chat_id, msg)
    # show_download_status(chat_id)
    return


def show_download_status(chat_id):
    global all_download_status
    x = str(all_download_status)
    print(f"\n\nsending download status:\n{x}")
    # bot.send_message(chat_id, x)

def get_chat_id(message):
    chat =  message.chat
    chat_id = getattr(chat, "id")
    return chat_id
# @server.route('/' + TOKEN, methods=['POST'])
# def getMessage():
#    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#    return "!", 200

# @server.route("/")
# def webhook():
#    bot.remove_webhook()
#    bot.set_webhook(url=heroku_web_url + TOKEN)
#    return "!", 200
# if __name__ == "__main__":
#    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


# POOLING....
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print("BOT GOT RUNTIME EXCEPTION EXITING...")
        exit()
        