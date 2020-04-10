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

request_queue = []
download_engine_status = False

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

@bot.message_handler(commands=['status'])  # help message handler
def status_send(message):
    chat_id = get_chat_id(message)
    show_download_status(chat_id)

@bot.message_handler(commands=['status_clear'])  # help message handler
def clear_status(message):
    # chat_id = get_chat_id(message)
    send_delete_clean_msg(message, 'status')

   
@bot.message_handler(commands=['d'])  # help message handler
def name_download(message):
    # bot.reply_to(message, 'download started...')
    fulltext = message.text[3:].split('@')
    if((fulltext[1] is None) or ('json' not in fulltext[1])):
        return bot.reply_to(message, "vimeo url err")
    if(fulltext[0] is None):
        return bot.reply_to(message, "filename err")

    global request_queue

    request_queue.append({'name':fulltext[0],'url': fulltext[1] , 'status':'got request'})
    print(f"GOT DOWNLOAD REQ, all requests")
    print(request_queue)
    check_start_engine()


# def download_request(file_name, master_json_url, message):
#     global request_queue
#     print(type(request_queue.keys))
#     time.sleep(30)
#     print("Downloaded file now deleting key from request_queue.")
#     print(f"before_delete :: {request_queue}")
#     del request_queue[file_name]
#     print(f"after_delete :: {request_queue}")


# def download_engine():
#     print("Engine Started\n\n")
#     global download_engine_status
#     global request_queue
#     download_engine_status = True
#     for key in request_queue:
#         print(f"\n\nEngine:: Downloading File .... {request_queue[key]['name']}")
        
#         time.sleep(30)
#         print(f"Engine:: Downloaded File .... {request_queue[key]['name']}\n")
#         print(f"before_delete Dict:: {request_queue}")
#         del request_queue[key]['name']
#         print(f"after_delete Dict:: {request_queue}")


#     print("\n\nEngine Closed..")
#     download_engine_status = False


def check_start_engine():
    global download_engine
    if(download_engine == True):
        print("Download Engine Already ON.")
        return
    else:
        print("Download Engine Switching ON")
        download_engine()


def download_engine():
    global download_engine_status
    global request_queue
    print(f"Download Engine  Started : {request_queue}")
    download_engine_status = True
    while download_engine_status:
        print(f"Download Engine : {request_queue}")
        if(len(request_queue) !=0):
            current_downloading  = request_queue[0]
            print(f"Some stuff there to download, downloading {current_downloading}")
            download_req()
            request_queue.remove(current_downloading)
            print(f"Deleted Current downloadig {current_downloading}")
            print(f"Present All Download status :: {request_queue} ")
        else:
            print("request queue is empty so closing engine..")
            download_engine_status = False
    print("Download engine shutdown")

def download_req():
    time.sleep(30)


def send_delete_clean_msg(message, msg):
    chat_id = get_chat_id(message)
    bot.send_message(chat_id, msg)
    # show_download_status(chat_id)
    return


def show_download_status(chat_id):
    global request_queue
    x = str(request_queue)
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
        