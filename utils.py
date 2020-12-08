import os
import shutil
import subprocess
import uuid
from pathlib import Path
from urllib.request import urlretrieve
import sys
import traceback
from bot import Bot

TEMP_PATH = "/temptracks"


def clean(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def create_dir(path):
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)


class Logger(object):
    def __init__(self):
        self.final_destination = ''
        self.log = ''

    def warning(self, msg):
        self.log += msg + '\n'
        print('[WARN] ' + msg)

    def error(self, msg):
        self.log += msg + '\n'
        print('[ERROR] ' + msg)

    def debug(self, msg):
        self.log += msg + '\n'
        ffmpeg_destination = '[ffmpeg] Destination: '
        if ffmpeg_destination in msg:
            self.final_destination = msg.replace(ffmpeg_destination, '')
        return print('[INFO] ' + msg)


def get_cover_art(url, extension='jpg'):
    MYDIR = os.path.dirname(__file__)
    file_path = f'{MYDIR}/{TEMP_PATH}/{str(uuid.uuid1())}.{extension}'
    create_dir(file_path)
    urlretrieve(url, file_path)
    return file_path


def check_ffmpeg():
    try:
        subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-hide_banner'], stdout=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print('Ffmpeg not found, please download and install to use Savify!')
        return False


def check_file(path):
    if Path(path).is_file():
        return True
    else:
        return False
