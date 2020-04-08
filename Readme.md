# Ptyton Telegram Vimeo Download BOT
Bot will download the vimeo video by master.json url and uploads that file in googledrive and telegram group you mentioned

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Steps to build bot.

  - Bot connection with googledrive
  - Bot connection with telegram
  - Heroku app deployment

## Bot Connection with Google Drive Account
  - create a project in [Google cloud console](https://console.cloud.google.com/)
  - create an api :: "Desktop app" 
  - create OAuth2.0 Credential :: [Apis credentials](https://console.cloud.google.com/apis/credentials)
  - download credentials and save them in repo as ``credentials.json`` << replace this file in the repo with your credentials
  - enable google drive for your api, [google drive api enable](https://console.cloud.google.com/apis/library/drive.googleapis.com)
  - install dependencies :: `` pip install -r requirements_initial.txt``
  - run file ``drive_auth.py`` >> this will open browser and ask to connect a google drive account yours and ask you allow permissions. allow them. Then the token will be save in the folder for accessing api to your drive.
 - replace to varialble values in ``bot.py`` 
  ``default_dir = '16m8_vJaE--4LluddsdsVP86j1XrAkT'``
 ``current_set_dir = '16m8_vJaE--4LludRLgfgZNSVVP86j1XrAkT'``
 replace with your drive folder where you want to upload downloaded files. 


## Bot Connection with Telegram
  - create a telegram bot and get the token and replace ``bot.py`` variable
    ``TOKEN = "114868821s46s0:AAGfLhk0asrKp5SPzTCwsdsddcgWJ2tYQngDBms1H4"``
  - replace ``grp_Chat_id = '-47824269081'`` to the grp where you want the bot to upload the files.

## heroku deployment
- go to repo folder open terminal 
- run cmd in command line : ``heroku login``
- login in into heroku website and ``create heroku app``.
- run cmd  : ``heroku git:remote -a <<Your heroku app name>>``
- run cmd  : ``heroku create``
- run cmd : ``heroku create --buildpack https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git``
- run cmd : ``heroku buildpacks``
- run cmd  : ``heroku info``
- after this command you will see something like this in log 
``Web URL:        https://your-heroku-app.herokuapp.com/`` 
copy this url and replace in ``bot.py``
variable : ``heroku_web_url = 'https://your-heroku-app.herokuapp.com/'``
- run cmd : ``git add * && git commit -m "First deploy"``
- run cmd : ``git push heroku master``
- run cmd : ``heroku logs -t``
- open url the url in browser. >> ``https://your-heroku-app.herokuapp.com/``
- Bot will be running ... : )




| References | Links |
| ------ | ------ |
| Google Apis Quick Start | https://developers.google.com/drive/api/v3/quickstart/python
| Medium Article for deployment to heroku | https://medium.com/@matt95.righetti/build-your-first-telegram-bot-using-python-and-heroku-79d48950d4b0 |
| Pyton Telegram Api  | https://github.com/eternnoir/pyTelegramBotAPI |







### Future update 
 - Clean chat messages by bro


License
----

MIT


**Free Software, Hell Yeah!**
