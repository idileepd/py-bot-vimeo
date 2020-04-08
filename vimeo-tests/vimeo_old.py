#!/usr/bin/env python
# Downloads the video and audio streams from the master json url and recombines
# it into a single file
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
        FFMPEG_BIN = 'ffmpeg'


def download_video(base_url, content):
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


def download_audio(base_url, content):
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


def merge_audio_video(output_filename):
    print("\n\n\n<<<<<<<<<<<<<  MERGE VIDEO AUDIO FUNCTION  >>>>>>>>>>>>>>>>>>")
    audio_filename = os.path.join(TEMP_DIR, OUT_PREFIX, "a.mp3")
    video_filename = os.path.join(TEMP_DIR, OUT_PREFIX, "v.mp4")
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


if __name__ == "__main__":
    print("\n\n<<<<<<<<<<<<<<<<<<< MAIN :)) >>>>>>>>>>>>>>>>>")

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", action="store", help="master json url")
    parser.add_argument("-o", "--output", action="store",
                        help="output video filename without extension (mp4)",
                        default=None)
    parser.add_argument("-s", "--skip-download", action="store",
                        help="merges video and audio output of already downloaded streams",
                        metavar="TIMESTAMP")
    parser.add_argument("--skip-merge", action="store_true",
                        help="downloads only and doesn't merge")
    args = parser.parse_args()

    # Set output filename depending on defaults
    if args.output:
        output_filename = os.path.join(OUTPUT_DIR, args.output + '.mp4')
    else:
        output_filename = os.path.join(
            OUTPUT_DIR, '{}_video.mp4'.format(OUT_PREFIX))
    print("Output filename set to:", output_filename)

    if not args.skip_download:
        print("<< NOT >> SKIPING THE DOWNLOAD ....")
        master_json_url = args.url  # DUDE URL<<<<

        # get the content
        resp = requests.get(master_json_url)

        #check the master.json is valid ot not.
        if resp.status_code != 200:
            print("GOT RESPONSE NOT 200 of master json. :(( ")
            match = re.search('<TITLE>(.+)<\/TITLE>',
                              resp.content, re.IGNORECASE)
            title = match.group(1)
            print('HTTP error (' + str(resp.status_code) + '): ' + title)
            print("QUITING....")
            quit(0)

        print("GOT Content from MASTER.json saving content...")
        content = resp.json()
        base_url = urlparse.urljoin(master_json_url, content['base_url'])

        # Download the components of the stream
        print("DOWNLOADING VIDEO AND AUDIO BY Calling the functions...")
        if not download_video(base_url, content['video']) or not download_audio(base_url, content['audio']):
            print("Unable to download video or audio... :(")
            print("Quitting...")
            quit()

    # Overwrite timestamp if skipping download
    if args.skip_download:
        print("SKIPING THE DOWNLOAD ....")
        TIMESTAMP = args.skip_download
        print("Overriding timestamp with:", TIMESTAMP)

    # Combine audio and video
    if not args.skip_merge:
        print("<NOT>SKIPING THE MERGING ....")
        merge_audio_video(output_filename)
