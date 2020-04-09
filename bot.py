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

download_completed_files = []
logs = []


#removing output and temp files
print("\n\n Removing Output directory and Temp directory")
if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
    print('removing output directory')
    shutil.rmtree(OUTPUT_DIR)

if os.path.exists(TEMP_DIR) and os.path.isdir(TEMP_DIR):
    print('removing temp directory')
    shutil.rmtree(TEMP_DIR)

print('Bot Started :)')



@bot.message_handler(commands=['start']) 
def send_welcome(message):
    print(f"\n\n Start MEssage :: \n{message}\n\n")
    send_chat_message(message, 'welcome to glat to see you. \n what you will download today Bro. \n\n '+ get_help_message())

@bot.message_handler(commands=['shutdown'])  
def exit_program(message):
    print("Exiting program")
    send_chat_message(message, 'shutting down bot')
    bot.stop_bot()
    quit()

@bot.message_handler(commands=['help'])
def send_help(message):
    msg = get_help_message()
    send_chat_message(message, msg)


@bot.message_handler(commands=['change_dir']) 
def change_download_drive_dir(message):
    folder_id = message.text[11:]
    print(folder_id)
    print("ASSUMING Folder exist bro...")
    global current_set_dir
    current_set_dir = folder_id
    print("Current Set Dir ", current_set_dir)
    send_chat_message(message, '\nCurrent Directory Id:\n'+current_set_dir)


@bot.message_handler(commands=['reset_dir'])
def reser_download_drive_dir(message):
    folder_id = message.text[11:]
    print(folder_id)
    global current_set_dir
    global default_dir
    current_set_dir = default_dir
    print("Reset to default directory", current_set_dir)
    send_chat_message(message, '\nCurrent Directory Id:\n'+current_set_dir)


@bot.message_handler(commands=['current_dir']) 
def current_download_drive_dir(message):
    print("Current Dir ", current_set_dir)
    send_chat_message(message, '\nCurrent Directory Id:\n'+current_set_dir)

@bot.message_handler(commands=['files'])
def get_files(message):
    send_chat_message(message, get_downloaded_files_list())

@bot.message_handler(commands=['logs'])
def get_logs_handler(message):
    count = message.text[6]
    try:
        send_chat_message(message, 'Logs: \n'+get_logs(int(count)))
    except:
        send_chat_message(message, 'Error occured..')



@bot.message_handler(commands=['d'])  
def name_download(message):
    try:
        fulltext = message.text[3:].split('@')
        if((fulltext[1] is None) or ('json' not in fulltext[1])):
            return bot.reply_to(message, "💥💥💥 vimeo url err")
        if(fulltext[0] is None):
            return bot.reply_to(message, "💥💥💥 filename err")
        download_request(fulltext[0], fulltext[1], message)
    except IndexError:
        send_chat_message(message, '💥💥💥\nFILENAME: '+fulltext[0]+'\nPlease check command.')
        print(f"\n\n\n\n\n {fulltext} command error of /d")
    except:
        print(f"\n\n\n\n\n {fulltext} Something err in download_request() function.")
        send_chat_message(message, '💥💥💥\nFILENAME: '+fulltext[0]+'\nSomething went wrong')



def download_request(file_name, json_url, message):
    global download_completed_files
    global logs


    logs.append('⭕ FILENAME: '+file_name+' > Download Started')
    print('⭕⭕⭕ \nFILENAME: '+file_name+'\nDwonload Started')
    send_chat_message(message, '⭕⭕⭕ \nFILENAME: '+file_name+'\nDwonload Started')
    #Downloading Vimeo File
    [download_status, dmsg] = vimeo.vimeo_downloader(json_url, file_name, False, False)


    if(download_status == True):

        print('🔵🔵🔵 \nFILENAME: '+file_name+'\nDownload Done')
        send_chat_message(message, '🔵🔵🔵 \nFILENAME: '+file_name+'\nDownload Done')
        logs.append('🔵 FILENAME: '+file_name+' > File Downloaded')

        #UPLOAD File TO GDRIVE
        global current_set_dir
        print(f'\n\n{file_name} uploading..  ::to folder :: {current_set_dir}')
        [upload_status, umsg]= drive.upload_video_to_this_folder(current_set_dir,file_name)
        if(upload_status == True):

            print('🔥🔥🔥 \nFILENAME: '+file_name+'\nUpload Done')
            send_chat_message(message, '🔥🔥🔥 \nFILENAME: '+file_name+'\nUpload Done')
            download_completed_files.append('✅ '+file_name)
            logs.append('✅ FILENAME: '+file_name+' > File Downloaded and Uploaded Completely')

        else:
            logs.append('💥 FILENAME: '+file_name+' > Upload failed Gdrive')
            send_chat_message(message, '💥💥💥\nFILENAME: '+file_name+'\nUpload failed Gdrive')
            print('💥💥💥\nFILENAME: '+file_name+'\nUpload failed Gdrive')
    else:
        logs.append('💥 FILENAME: '+file_name+' > Download failed')
        send_chat_message(message, '💥💥💥\n'+file_name+'Download failed')
        print('💥💥💥\nFILENAME: '+file_name+'Download failed')
    return


def send_chat_message(message, msg):
    chat_id = get_chat_id(message)
    bot.send_message(chat_id, msg)
    return

def get_downloaded_files_list():
    global download_completed_files
    messgae = 'Downloaded Files are :\n'
    for filename in download_completed_files:
        messgae = messgae+filename+ '\n'
    return messgae


def get_chat_id(message):
    chat =  message.chat
    chat_id = getattr(chat, "id")
    return chat_id


def get_logs(count):
    global logs
    flogs = []
    if(count<=len(logs)):
        flogs = logs
    else:
        flogs = logs[-count:]
    message = ''
    for log in flogs:
        message = message+'\n'+log
    return message    


def get_help_message():
    msg = 'List of Commands are :\n'
    msg = msg + '/d - cmd to download vimeo file with name and link seperated by @\n'
    msg = msg + '   Ex: /d <<you_file_name>>@<<download_url>>\n\n'
    msg = msg + '/current_dir - get current google drive directory \n'
    msg = msg + '/reset_dir - reset google  drive downlaod directory to defult \n'
    msg = msg + '/change_dir - change the current directory to your specified directory\n'
    msg = msg + '   Ex: /change_dir <<drive_dir_name>>\n\n'
    msg = msg + '/files - get all downloaded files\n'
    msg = msg + '/logs - get logs of specified count\n'
    msg = msg + '   Ex: /logs <<count_val>>\n\n'
    msg = msg + '/shutdown - shutdown the bot\n'
    msg = msg + '/help - get help from me'

    return msg

# POOLING....
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print("BOT GOT RUNTIME EXCEPTION EXITING...")
        exit()
        