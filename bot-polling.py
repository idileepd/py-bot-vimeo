import time
import telebot
import os
import sys
import drive_api as drive
import vimeo_api as vimeo

TOKEN = "1148821460:AAGfLhk0rKp5SPzTCwcgWJ2tYQngDBms1H4"
bot = telebot.TeleBot(token=TOKEN)
# server = Flask(__name__)

default_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'
current_set_dir = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'

grp_Chat_id = '-478269081'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# heroku_web_url = 'https://py-bot-vimeo.herokuapp.com/'

print("Bot Started :)")


@bot.message_handler(commands=['start'])  # welcome message handler
def send_welcome(message):
    print(f"\n\n Start MEssage :: \n{message}\n\n")
    bot.reply_to(message, 'hii welcome!!!')

@bot.message_handler(commands=['help'])  # help message handler
def send_help(message):
    bot.reply_to(
        message, '/d - cmd to download vimeo file with name \n Ex: /d fileName@http://vimep..json\n/dd - cmd to direct download file\n\n/help - help cmd')




# @bot.message_handler(commands=['dddd'])  # help message handler
# def direct_download(message):
#     bot.reply_to(message, 'download started...')
#     print(message.text[4:])
#     masterJson = message.text[4:]


    # try:
    #     os.system("python vimeo-download.py --url "+masterJson)
    #     bot.reply_to(message, "Downlod completed !😍😍😍😍\n"+get_all_file())
    # except:
    #     print("An exception occurred")
    #     bot.reply_to(message, "Downlod ERROR :(( !")





@bot.message_handler(commands=['upload-test'])
def upload_test_vdo(message):
    # chat = message.chat
    # chat_id  = getattr(chat, 'id')
    # print("Uploading video..")
    # BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    # OUTPUT_DIR = os.path.join(BASE_DIR, "output\\test.mp4")
    # video = open(OUTPUT_DIR, 'rb')
    # print("Got video reference")
    # bot.send_video(chat_id, video)
    # print("Sending vdo")
    upload_video_to_grp('newfinaltest', message)
    # bot.send_video(chat_id, "FILEID")


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



# @bot.message_handler(commands=['d'])  # help message handler
# def name_download(message):
#     try:
#         # bot.reply_to(message, 'download started...')
#         fulltext = message.text[3:].split('@')
#         if((fulltext[1] is None) or ('json' not in fulltext[1])):
#             return bot.reply_to(message, "vimeo url err")
#         if(fulltext[0] is None):
#             return bot.reply_to(message, "filename err")

#         download_request(fulltext[0], fulltext[1], message)
        
#     except IndexError:
#         bot.reply_to(message, "Please check command.")
#         print(f"\n\n\n\n\n {fulltext} command error of d")
#     except:
#         print(f"\n\n\n\n\n {fulltext} command error of d")
#         bot.reply_to(message, "something went wrong")

@bot.message_handler(commands=['d'])  # help message handler
def name_download(message):
    
    # bot.reply_to(message, 'download started...')
    fulltext = message.text[3:].split('@')
    if((fulltext[1] is None) or ('json' not in fulltext[1])):
        return bot.reply_to(message, "vimeo url err")
    if(fulltext[0] is None):
        return bot.reply_to(message, "filename err")

    download_request(fulltext[0], fulltext[1], message)



def download_request(file_name, master_json_url, message):
    bot.reply_to(message, file_name+'::\n Download just started.')
    # 1. download the file 
    # 2. upload to drive, (if possible upload to agrp or to user.)
    # 3. send drive link or id anything
    [download_status, download_message] = vimeo.vimeo_downloader(master_json_url, file_name, False, False)
    print(f"download status :: {download_status}")
    print(f"download message :: {download_message}")
    if(download_status == True):
        bot.reply_to(message, file_name+'\n::Download video part over. \n Now Uploading to GoogleDrive')
        # upload file to telegram for now.
        # upload to drive
        # [upload_status, upload_message]= drive.upload_video_to_my_folder(download_message)

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

        # UPLOAD TO VDOS GRP
        [grp_upload_status, grp_upload_message] = upload_video_to_grp(file_name, message)
        if(grp_upload_status == True):
            bot.reply_to(message, file_name+'\n::File Downloaded and Uploaded in drive and telegram Successfully')
        else:
            bot.reply_to(message, grp_upload_message)

    else:
        bot.reply_to(message, download_message)
    return


# def upload_video_to_grp(file_name, message):
#     try:
#         file_name = file_name+'.mp4'
#         global grp_Chat_id
#         global OUTPUT_DIR
#         file_path = os.path.join(OUTPUT_DIR, file_name)
#         file_path = '/'.join(file_path.split('\\'))
#         print(f"File path : {file_path}")
#         print("Uploading video.. to telegram grp")
#         bot.reply_to(message, file_name+'\n::Now Uploading to TelegramGroup')
#         video = open(file_path, 'rb')
#         print("Got video reference")
#         print("Sending vdo...")
#         bot.send_video(grp_Chat_id, video, caption=file_name)
#         print(f'uploaded  video in telegram grp:: {file_name}')
#         print(f"Deleting file Locally :: {file_name}")
#         video.close()
#         os.remove(file_path)
#         return [True, file_name+'\n video sent to grp successfully']
#     except:
#         print(f"\n\n\n\n\n {file_name} <<<<<<< ERROR OCCURED IN UPLOAD VIDEO TO TELEGRAM GRP ")
#         return [False, file_name+'\n Failed to upload video to telegram grp']

def upload_video_to_grp(file_name, message):
    file_name = file_name+'.mp4'
    global grp_Chat_id
    global OUTPUT_DIR
    file_path = os.path.join(OUTPUT_DIR, file_name)
    file_path = '/'.join(file_path.split('\\'))
    print(f"File path : {file_path}")
    print("Uploading video.. to telegram grp")
    bot.reply_to(message, file_name+'\n::Now Uploading to TelegramGroup')
    video = open(file_path, 'rb')
    print("Got video reference")
    print("Sending vdo...")
    bot.send_video(grp_Chat_id, video, caption=file_name)
    print(f'uploaded  video in telegram grp:: {file_name}')
    print(f"Deleting file Locally :: {file_name}")
    video.close()
    os.remove(file_path)
    return [True, file_name+'\n video sent to grp successfully']


# POOLING....
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print("BOT GOT RUNTIME EXCEPTION EXITING...")
        exit()
        

