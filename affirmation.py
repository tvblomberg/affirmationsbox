#!/usr/bin/env python3
import glob
import os
import datetime
import configparser
import random
import RPi.GPIO as GPIO

config = configparser.ConfigParser()
config.read("affirmations.ini")

def get_str(name, default_value=None):
    try:
        return config.get("DEFAULT", name)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default_value


def get_affirmations_dir():
    return get_str("AFFIRMATIONS_DIR", os.path.dirname(os.path.realpath(__file__)))


def get_working_dir():
    return get_str("WORKING_DIR", os.path.dirname(os.path.realpath(__file__)))


def get_todays_folder_name():
    now = datetime.datetime.now()
    return now.strftime("%m%d%Y")


def get_todays_folder_path():
    return os.path.join(get_working_dir(), get_todays_folder_name())


def create_todays_folder():
    os.mkdir(get_todays_folder_path())


def today_exists():
    return os.path.exists(get_todays_folder_path())


def get_mp3s(folder_path):
    return glob.glob(os.path.join(folder_path, "*.mp4"))


def todays_affirmation_exists():
    return len(get_mp3s(get_todays_folder_path())) > 0


def get_todays_affirmation():
    affirmations = get_mp3s(get_todays_folder_path())
    return None if len(affirmations) == 0 else affirmations[0]


def pick_affirmation():
    files = get_mp3s(get_working_dir())
    file_count = len(files)

    if file_count > 0:
        file_num = random.randint(0, file_count - 1)
        return files[file_num]

    return None


def move_affirmation(file):
    if file != None:
        head, tail = os.path.split(file)
        os.rename(file, os.path.join(get_todays_folder_path(), tail))


def play(file):
    if file != None:
        os.system('/usr/bin/omxplayer -o alsa:hw:0,0 ' + file)


def main():
    if today_exists() == False:
        create_todays_folder()

    if todays_affirmation_exists() == False:
        move_affirmation(pick_affirmation())

    play(get_todays_affirmation())

def button_callback(channel):
    main()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)