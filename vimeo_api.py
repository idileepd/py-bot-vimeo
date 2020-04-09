from __future__ import print_function
import requests
import base64
from tqdm import tqdm
import sys
import subprocess as sp
import os
import distutils.core
import argparse
import urllib.parse as urlparse
import datetime

import random
import string
import re
import shutil

print("MY VIMEO DOWNLOADER IMPORTED")


def download_video(base_url, content, INSTANCE_TEMP, ):
    """Downloads the video portion of the content into the INSTANCE_TEMP folder"""
    print("\n\n\n<<<<<<<<<<<<<  DOWNLOAD VIDEO FUNCTION  >>>>>>>>>>>>>>>>>>")
    print("Downloads the video portion of the content into the INSTANCE_TEMP folder")
    result = True
    heights = [(i, d['height']) for (i, d) in enumerate(content)]
    idx, _ = max(heights, key=lambda t: t[1])
    video = content[idx]
    video_base_url = urlparse.urljoin(base_url, video['base_url'])
    print('video base url::: ', video_base_url)

    # Create INSTANCE_TEMP if it doesn't exist
    if not os.path.exists(INSTANCE_TEMP):
        print("Creating INSTANCE_TEMP FOLDER :::  {}...".format(INSTANCE_TEMP))
        os.makedirs(INSTANCE_TEMP)

    # Download the video portion of the stream
    filename = os.path.join(INSTANCE_TEMP, "v.mp4")
    filename = '/'.join(filename.split('\\'))
    # print('saving to %s' % filename)
    print(f'Saving to ::: {filename}')
    video_file = open(filename, 'wb')

    init_segment = base64.b64decode(video['init_segment'])
    video_file.write(init_segment)

    for segment in tqdm(video['segments']):
        segment_url = video_base_url + segment['url']
        resp = requests.get(segment_url, stream=True)
        if resp.status_code != 200:
            print('RESPONSE STATUS :::: NOT 200 :(')
            print(f'RESPONSE IS :::: {resp}')
            print(f'SEGMENT URL :::: {segment_url}')
            result = False
            break
        for chunk in resp:
            video_file.write(chunk)

    video_file.flush()
    video_file.close()
    print(f'Result of download video :::: {result} ')
    return result


def download_audio(base_url, content, INSTANCE_TEMP):
    """Downloads the video portion of the content into the INSTANCE_TEMP folder"""
    print("\n\n\n<<<<<<<<<<<<<  DOWNLOAD AUDIO FUNCTION  >>>>>>>>>>>>>>>>>>")
    print("Downloads the video portion of the content into the INSTANCE_TEMP folder")
    result = True
    audio = content[0]
    audio_base_url = urlparse.urljoin(base_url, audio['base_url'])
    print('audio base url:::', audio_base_url)

    # Create INSTANCE_TEMP if it doesn't exist
    if not os.path.exists(INSTANCE_TEMP):
        print("Creating INSTANCE_TEMP FOLDER ::: {}...".format(INSTANCE_TEMP))
        os.makedirs(INSTANCE_TEMP)

    # Download
    filename = os.path.join(INSTANCE_TEMP, "a.mp3")
    filename = '/'.join(filename.split('\\'))
    # print('saving to %s' % filename)
    print(f'Saving to ::: {filename}')

    audio_file = open(filename, 'wb')

    init_segment = base64.b64decode(audio['init_segment'])
    audio_file.write(init_segment)

    for segment in tqdm(audio['segments']):
        segment_url = audio_base_url + segment['url']
        resp = requests.get(segment_url, stream=True)
        if resp.status_code != 200:
            print('RESPONSE STATUS :::: NOT 200 :(')
            print(f'RESPONSE IS :::: {resp}')
            print(f'SEGMENT URL :::: {segment_url}')
            result = False
            break
        for chunk in resp:
            audio_file.write(chunk)

    audio_file.flush()
    audio_file.close()
    print(f'Result of download audio :::: {result} ')
    return result


def merge_audio_video(output_filename, TEMP_DIR, OUT_PREFIX, FFMPEG_BIN, OS_WIN, INSTANCE_TEMP):
    print("\n\n\n<<<<<<<<<<<<<  MERGE VIDEO AUDIO FUNCTION  >>>>>>>>>>>>>>>>>>")
    audio_filename = os.path.join(TEMP_DIR, OUT_PREFIX, "a.mp3")
    video_filename = os.path.join(TEMP_DIR, OUT_PREFIX, "v.mp4")

    audio_filename = '/'.join(audio_filename.split('\\'))
    video_filename = '/'.join(video_filename.split('\\'))

    
    command = [FFMPEG_BIN,
               '-i', audio_filename,
               '-i', video_filename,
               '-acodec', 'copy',
               '-vcodec', 'copy',
               output_filename]
    print("ffmpeg command is::::", command)

    if OS_WIN:
        sp.call(command, shell=True)
    else:
        sp.call(command)
    shutil.rmtree(INSTANCE_TEMP)
    return True


# We will send url, outputfilename (without extension) and false, false
def vimeo_downloader(args_url, args_output, args_skip_download, args_skip_merge):
    # -----------------------------------------INITIAL SETTINGS--------------------------------
    # Prefix for this run
    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    SALT = ''.join(random.choice(string.digits) for _ in range(3))
    OUT_PREFIX = TIMESTAMP + '-' + SALT
    print("<<<<<<<<---------Prefix-------->>>>>>")
    print(f'Timestamp: {TIMESTAMP} \nSalt: {SALT} \nOUT_PREFIX: {OUT_PREFIX}')

    # Create temp and output paths based on where the executable is located
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")


    # conver sting paths..
    BASE_DIR = '/'.join(BASE_DIR.split('\\'))
    TEMP_DIR = '/'.join(TEMP_DIR.split('\\'))
    OUTPUT_DIR = '/'.join(OUTPUT_DIR.split('\\'))

    print("<<<<<<<<---------Setting Temp, Output Directories PATHS -------->>>>>>")
    print(
        f'BASE_DIR: {BASE_DIR} \n TEMP_DIR: {TEMP_DIR} \n OUTPUT_DIR: {OUTPUT_DIR}')

    print("<<<<<<<<---------Creating temp, output dirs if they don't exist -------->>>>>>")
    for directory in (TEMP_DIR, OUTPUT_DIR):
        if not os.path.exists(directory):
            print("Creating {}...".format(directory))
            os.makedirs(directory)

    # create temp directory right before we need it
    INSTANCE_TEMP = os.path.join(TEMP_DIR, OUT_PREFIX)
    INSTANCE_TEMP = '/'.join(INSTANCE_TEMP.split('\\'))
    
    print(
        f"<<<<<<<<---------setting Instance temp dir, dir that right before we need :: {INSTANCE_TEMP} -------->>>>>>")

    # Check operating system
    OS_WIN = True if os.name == "nt" else False

    # Find ffmpeg executable
    if OS_WIN:
        FFMPEG_BIN = 'ffmpeg.exe'
    else:
        try:
            FFMPEG_BIN = distutils.spawn.find_executable("ffmpeg")
        except AttributeError:
            print(f"\n\n\n FFMPEG ERROR :( ")
            FFMPEG_BIN = 'ffmpeg'

    # ----------------------------------------------------------------------------------------------------------------

    # ---------------------------------------Download stuff --------------------------------------------

    # Set output filename depending on defaults
    # if args.output:
    #     output_filename = os.path.join(OUTPUT_DIR, args.output + '.mp4')
    # else:
    #     output_filename = os.path.join(
    #         OUTPUT_DIR, '{}_video.mp4'.format(OUT_PREFIX))
    output_filename = os.path.join(OUTPUT_DIR, args_output + '.mp4')
    output_filename = '/'.join(output_filename.split('\\'))
    print("Output filename set to:", output_filename)

    if not args_skip_download:
        print("<< NOT >> SKIPING THE DOWNLOAD ....")
        master_json_url = args_url  # DUDE URL<<<<

        # get the content
        resp = requests.get(master_json_url)

        # check the master.json is valid ot not.
        if resp.status_code != 200:
            print("GOT RESPONSE NOT 200 of master json. :(( ")
            match = re.search('<TITLE>(.+)<\/TITLE>',
                              resp.content, re.IGNORECASE)
            title = match.group(1)
            print('HTTP error (' + str(resp.status_code) + '): ' + title)
            print("QUITING....")
            return [False, 'http error for master.json request']
            # quit(0)

        print("GOT Content from MASTER.json saving content...")
        content = resp.json()
        base_url = urlparse.urljoin(master_json_url, content['base_url'])

        # Download the components of the stream
        print("DOWNLOADING VIDEO AND AUDIO BY Calling the functions...")
        if not download_video(base_url, content['video'], INSTANCE_TEMP) or not download_audio(base_url, content['audio'], INSTANCE_TEMP):
            print("Unable to download video or audio... :(")
            """ BOT REPLY UNABLE TO DOWNLOAD VIDEO OR AUDIO.."""

            print("Quitting...")
            return [False, 'Unable to download video or audio...']
            # quit()

    # Overwrite timestamp if skipping download
    if args_skip_download:
        print("SKIPING THE DOWNLOAD ....")
        TIMESTAMP = args_skip_download
        print("Overriding timestamp with:", TIMESTAMP)

    # Combine audio and video
    if not args_skip_merge:
        print("<NOT>SKIPING THE MERGING ....")
        merge_audio_video(output_filename, TEMP_DIR, OUT_PREFIX,
                          FFMPEG_BIN, OS_WIN, INSTANCE_TEMP)

    """ BOT REPLY DOWNLOAD COMPLETED .."""
    print("DOWNLOAD COMPLETED ....... <<<<<<<<<<<<<< ")
    """ BOT REPLY Uploading.. and tell  COMPLETED .."""

    print("Write upload file and delete file...")

    return [True, args_output]

# url = 'https://176vod-adaptive.akamaized.net/exp=1586442265~acl=%2F359281775%2F%2A~hmac=4b4c9128d176053686cb6427dc8cf7f1b50cea9c7e61f90099b05e30efbda2c6/359281775/sep/video/1472693452,1472693451,1472680057,1472680054,1472680048/master.json?base64_init=1'
# fname = 'test1'
# vimeo_downloader(url, fname, False, False)
 