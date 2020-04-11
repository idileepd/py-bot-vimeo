import time
import telebot
import os
import sys
import drive_api as drive
import vimeo_api as vimeo
import shutil
from slugify import slugify
import drive_upload as drive_upload
#SERVER MODE
# from flask import Flask, request
# server = Flask(__name__)
# heroku_web_url = 'https://py-bot-vimeo.herokuapp.com/'



# Pybot bot adv token
TOKEN = "1161305170:AAHibSPAJOtk-7yi1FcA8WIlYDOGh5XC-e8"
# bot = telebot.TeleBot(token=TOKEN)
bot = telebot.AsyncTeleBot(token=TOKEN)


dileep = 760135118
venu = 642649878
kamesh = 599072894
allowed_grp = -1001413818920
allowed_users_grp = [dileep, allowed_grp, venu,]

# allowed_grp = -322400391


default_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'
current_set_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'



BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

download_completed_files = []
download_failed_files = []
upload_failed_files = []
logs = []

bot_downloding_status = False



print('Bot Started :)')






@bot.message_handler(commands=['add']) 
def add_grp_user_handle(message):
    print("\n\n\nGOT ADD REQUEST >>")
    if isAllowed(message)!=True:
        send_chat_message(message, 'You are not Authorized')
        return
    print(f"ALLOWING USER ID OR GRP ID:: {message.text.split(' ')[1]}")
    allow_this_grp_user(int(message.text.split(' ')[1]), message)

@bot.message_handler(commands=['start']) 
def send_welcome(message):
    print("\n\n\n<<GOT START REQUEST>>")
    if isAllowed(message)!=True:
        send_chat_message(message, 'You are not Authorized')
        return
    global bot_downloding_status
    if bot_downloding_status == False:
        print(f"\n\n Start MEssage :: \n{message}\n\n")
        send_chat_message(message, 'welcome to glad to see you. \n what you will download today \n😀')
    else:
        send_chat_message(message, '✋✋✋\n 🛑🛑🛑\n wait, \n Bot is Busy')
    


@bot.message_handler(commands=['files'])
def get_files(message):
    print("\n\n\n<< GOT FILES REQUEST >>")
    if isAllowed(message)!=True:
        send_chat_message(message, 'You are not Authorized')
        return
    global bot_downloding_status
    if bot_downloding_status == False:
        send_chat_message(message, get_output_dir_files())
    else:
        send_chat_message(message, '✋✋✋\n 🛑🛑🛑\n wait, \n Bot is Busy.')



@bot.message_handler(commands=['shutdown'])  
def exit_program(message):
    print("Exiting program")
    send_chat_message(message, 'shutting down bot')
    bot.stop_bot()
    sys.exit("Bot Shudown...")


@bot.message_handler(commands=['d'])  
def name_download(message):
    print("\n\n\n<< GOT DOWNLOAD VIDEO REQ >>")
    if isAllowed(message)!=True:
        send_chat_message(message, 'You are not Authorized')
        return
    global bot_downloding_status
    if bot_downloding_status == False:
        try:
            # bot_downloding_status =True
            fulltext = message.text[3:].split('@')
            if((fulltext[1] is None) or ('json' not in fulltext[1])):
                return bot.reply_to(message, "💥💥💥 vimeo url err")
            if(fulltext[0] is None):
                return bot.reply_to(message, "💥💥💥 filename err")
            fulltext[0] = slugify(fulltext[0])

            download_request(fulltext[0], fulltext[1], message)        
        except IndexError:
            send_chat_message(message, '💥💥💥\nFILENAME: '+fulltext[0]+'\nPlease check command.')
            print(f"\n\n\n\n\n {fulltext} command error of /d")
        except:
            print(f"\n\n\n\n\n {fulltext} Something err in download_request() function.")
            send_chat_message(message, '💥💥💥\nFILENAME: '+fulltext[0]+'\nSomething went wrong')
        # finally:
        #     # bot_downloding_status = False
    else:
        send_chat_message(message, '✋✋✋\n 🛑🛑🛑\n wait, \n Bot is Busy.')


# @bot.message_handler(commands=['upload'])
# def upload_files_handle(message):
#     print("\n\n\n<<Upload ALL Files REQUEST>>")
#     if isAllowed(message)!=True :
#         send_chat_message(message, 'You are not Authorized')
#         return
#     global bot_downloding_status
#     if bot_downloding_status == False:
#         bot_downloding_status = True
#         try:
#             send_chat_message(message, "Uploading files started..")
#             upload_allfiles(message)
#             send_chat_message(message, "Uploaded All Files...")
#         except:
#             bot.reply_to(message, "💥💥💥 \nerror Occured in uploading all files...!!\n")
#         finally:
#             bot_downloding_status = False
#     else:
#         send_chat_message(message, '✋✋✋\n wait, \n Bot is Busy. ')

@bot.message_handler(commands=['upload'])
def upload_files_handle(message):
    print("\n\n\n<<Upload ALL Files REQUEST>>")
    if isAllowed(message)!=True :
        send_chat_message(message, 'You are not Authorized')
        return
    global bot_downloding_status
    if bot_downloding_status == False:
        bot_downloding_status = True
        send_chat_message(message, "Uploading files started..")
        upload_allfiles(message)

    else:
        send_chat_message(message, '✋✋✋\n wait, \n Bot is Busy. ')


def upload_allfiles(message):
    if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        total_files = str(len(os.listdir(OUTPUT_DIR)))
        print(f"Total files {total_files}")

        for index, filename in enumerate(os.listdir(OUTPUT_DIR)):
            num = index+1
            print(f"\n\n\nCurrent File : {filename}")
            send_chat_message(message, str(num)+'/'+total_files+'\n Uploading File..\n'+filename)
            drive_upload.upload_video(filename)


        return "All files upload complete"
    else:
        send_chat_message(message, "No OUTPUT Directory Exist")
        return "No Directory Exist"


def get_output_dir_files():
    message = 'Downloaded files in output directory :\n'
    if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(".mp4"): 
                message = message +'\n>> '+ filename
                continue
            else:
                continue
        return message
    else:
        return "No Files present. (output directory is not present)"







def download_request(file_name, json_url, message):
    start = time.time()
    print('⭕⭕⭕ \n\n\n\nFILENAME: '+file_name+'\nDwonload Started')
    send_chat_message(message, '⭕⭕⭕ \nFILENAME: '+file_name+'\nDwonload Started')

    #Downloading Vimeo File
    [download_status, dmsg] = vimeo.vimeo_downloader(json_url, file_name, False, False)
    print(dmsg)

    if(download_status == True):
        print('🔵🔵🔵 \nFILENAME: '+file_name+'\nDownload Done\nTAKEN TIME ')
        taken_time = str((time.time()-start)/60)
        send_chat_message(message, '🔵🔵🔵 \nFILENAME: '+file_name+'\nDownload Done\nTAKEN TIME '+taken_time)
        return True
    else:
        send_chat_message(message, '💥💥💥\n'+file_name+'Download failed')
        print('💥💥💥\nFILENAME: '+file_name+'Download failed')
        return False


def clear_dirs():
    #removing output and temp files
    print("\n\n Removing Output directory and Temp directory")
    if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        print('removing output directory')
        shutil.rmtree(OUTPUT_DIR)

    if os.path.exists(TEMP_DIR) and os.path.isdir(TEMP_DIR):
        print('removing temp directory')
        shutil.rmtree(TEMP_DIR)

def send_chat_message(message, msg):
    chat_id = get_chat_id(message)
    bot.send_message(chat_id, msg)
    return


def get_chat_id(message):
    chat =  message.chat
    chat_id = getattr(chat, "id")
    return chat_id


def isAllowed(message):
    global allowed_grp
    # print(f"\n\n\n\n:::Checking Authorization :::")
    chat_id = get_chat_id(message)
    # print("Got chat ID:: "+str(chat_id))
    user_id = get_from_user_id(message)
    # print(f"GOT USER ID :: {user_id}")
    if(chat_id in allowed_users_grp or user_id in allowed_users_grp):
        print("Access Granted")
        return True
    else:
        print("Access Rejected")
        return False

def get_from_user_id(message):
    from_user = message.from_user
    # print(f"From User :: {from_user}")
    user_id = getattr(from_user, "id")
    return user_id

def allow_this_grp_user(grp_id, message):
    global allowed_users_grp
    allowed_users_grp.append(grp_id)
    send_chat_message(message, str(grp_id)+'\n::Group or user now allowed')
    print(f"Allowed Users or grps : \n{allowed_users_grp}")





# POOLING....
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print("BOT GOT RUNTIME EXCEPTION EXITING...")
        exit()
        




