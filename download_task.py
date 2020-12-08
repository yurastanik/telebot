import uuid
import ast
import ffmpy
import youtube_dl
from bot import Bot
from track import Track
from urllib.parse import urlparse
import vedisdb
import utils
from threading import Timer, Thread
import threading
import time
import requests
import os
import data
import sys
import traceback
import random


del_ls = []
act_dict = {}
clocks = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']
ditc = {}
thumbs = ['http://i.piccy.info/i9/7c2ebeceaf63b3d1b5ea8999922cc0ab/1593460967/92862/1385798/Mus.jpg',
          'http://i.piccy.info/i9/2043c40f07a4b2e01ece1244d1c653b3/1593460281/161804/1385798/Mus1.png']

res_av = threading.Event()
res_av.set()


def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute


@thread
def deleteFile(file):
    if not res_av.isSet():
        res_av.wait()
    res_av.clear()
    try:
        os.remove(file)
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
    res_av.set()


def video_id(url):
    try:
        o = urlparse(url)
        if o.netloc == 'youtu.be':
            return o.path[1:]
        elif o.netloc in ('www.youtube.com', 'youtube.com'):
            if o.path == '/watch':
                id_index = o.query.index('v=')
                return o.query[id_index + 2:id_index + 13]
            elif o.path[:7] == '/embed/':
                return o.path.split('/')[2]
            elif o.path[:3] == '/v/':
                return o.path.split('/')[2]
        return False
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        return False


def namevid(videoid):
    try:
        url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + str(videoid) + \
              '&key=AIzaSyDI9wePPlex74bPQLYwbwy5xL3EcXn9tXY'
        r = requests.get(url).json()
        name = r['items'][-1]['snippet']['title']
        art = r['items'][-1]['snippet']['channelTitle']
        thumb_list = r['items'][-1]['snippet']["thumbnails"]
        key = list(thumb_list.keys())[-1]
        thumb = r['items'][-1]['snippet']["thumbnails"][key]['url']
        return [art, name, thumb]
    except Exception:
        return ["Unknown artist", "Unknown song", random.choice(thumbs)]


@thread
def process(mes_id, artist, trackname, bot: Bot):
    try:
        flag = True
        for x in range(12):
            if act_dict.get(str(bot.chat_id) + str(mes_id)) is None:
                flag = False
                break
            bot.editMessageText(mes_id,
                                "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                       "обработка ролика</i>\n      %s "
                                                                       "<i>Подготовка к отправке</i>\n "
                                                                       "     ⏳ <i>Отправка аудиофайла</i>" % clocks[x])
        if flag:
            process(mes_id, artist, trackname, bot)
    except Exception:
        bot.editMessageText(mes_id,
                            "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                   "обработка ролика</i>\n      ✅ "
                                                                   "<i>Подготовка к отправке</i>\n "
                                                                   "     ⏳ <i>Отправка аудиофайла</i>")


@thread
def fakeprocess(mes_id, artist, trackname, bot: Bot, i=0, en=True):
    try:
        i += 1
        flag = True
        for x in range(12):
            if act_dict.get(str(bot.chat_id) + str(mes_id)) is None:
                flag = False
                bot.editMessageText(mes_id,
                                    "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                           "обработка ролика</i>\n      ✅ "
                                                                           "<i>Подготовка к отправке</i>\n "
                                                                           "     ✅ <i>Отправка аудиофайла</i>")
                break
            bot.editMessageText(mes_id,
                                "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                       "обработка ролика</i>\n      ✅ "
                                                                       "<i>Подготовка к отправке</i>\n "
                                                                       "     %s <i>Отправка аудиофайла</i>" % clocks[x])
        if flag:
            if i > 5:
                action(bot.chat_id, str(bot.chat_id) + str(mes_id))
            elif en:
                fakeprocess(mes_id, artist, trackname, bot, i)
        else:
            bot.editMessageText(mes_id,
                                "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                       "обработка ролика</i>\n      ✅ "
                                                                       "<i>Подготовка к отправке</i>\n "
                                                                       "     ✅ <i>Отправка аудиофайла</i>")
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def delmes(bot: Bot, mes_id1, mes_id2):
    try:
        bot.deleteMessage(mes_id1)
        if mes_id2 is not None:
            bot.deleteMessage(mes_id2)
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def action(chat_id, key):
    try:
        bot = Bot(chat_id)
        flag = act_dict.get(key)
        if flag:
            bot.sendChatAction()
            Timer(3, action, [chat_id, key]).start()
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


@thread
def download_task(quality, download_format, output_path, chat_id, mes_id, artist, trackname,
                  track: Track = None, url=None, thumb=None, mes_id2=None):
    MYDIR = os.path.dirname(__file__)
    output_path = f'{MYDIR}/{output_path}'
    try:
        logger = utils.Logger()
        bot = Bot(chat_id)
        delete_files = []
        if track:
            cid = track.id
        else:
            cid = video_id(url)

        def hook(information):
            try:
                downloaded = information['downloaded_bytes']
                finish = information['total_bytes']
                bot.editMessageText(mes_id,
                                    "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ⏳ <i>Загрузка и "
                                                                           "обработка ролика %s</i>\n      ⏳ "
                                                                           "<i>Подготовка к отправке</i>\n "
                                                                           "     ⏳ <i>Отправка аудиофайла</i>" %
                                    (str(int(float((int(downloaded) / int(finish))) * 100)) + '%'))
                if information['status'] == "finished":
                    bot.editMessageText(mes_id,
                                        "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                               "обработка ролика</i>\n      ⏳ "
                                                                               "<i>Подготовка к отправке</i>\n "
                                                                               "     ⏳ <i>Отправка аудиофайла</i>")
                    act_dict.update({str(chat_id) + str(mes_id): True})
                    process(mes_id, artist, trackname, bot)
            except Exception:
                return None

        correct_name = trackname

        if "\\" in trackname or "/" in trackname:
            correct_name = trackname.replace("\\", "?").replace("/", "?")

        output_path += f'{artist} - ' \
                       f'{correct_name}.{download_format}'
        delete_files.append(str(output_path))
        utils.create_dir(output_path)
        temp_file = str(uuid.uuid1())
        delete_files.append(f'{MYDIR}/{utils.TEMP_PATH}/{str(temp_file)}.mp3')
        options = {
            'format': 'bestaudio/best',
            'outtmpl': f'{MYDIR}/{utils.TEMP_PATH}/{str(temp_file)}.%(ext)s',
            'restrictfilenames': True,
            'nooverwrites': True,
            'noplaylist': True,
            'prefer_ffmpeg': True,
            'logger': logger,
            'progress_hooks': [hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': download_format,
                'preferredquality': quality,
            }],
            'postprocessor_args': [
                '-write_id3v1', '1',
                '-id3v2_version', '3',
                '-q:a', '3',
                '-metadata', f'title={trackname}',
                '-metadata', f'artist={artist}',
                '-codec:a', 'libmp3lame',
            ],
        }
        if track:
            query = str(track) + ' (AUDIO)'
            lst = ['-metadata', f'album={track.album_name}',
                   '-metadata', f'date={track.release_date}',
                   '-metadata', f'disc={track.disc_number}',
                   '-metadata', f'track={track.track_number}/{track.album_track_count}']
            options.update({'default_search': 'ytsearch'})
            for item in lst:
                options['postprocessor_args'].append(item)
        else:
            query = url
        with youtube_dl.YoutubeDL(options) as ydl:
            inf = ydl.extract_info(query, download=False)
            if inf.get("duration") is not None:
                if inf.get("duration") > 3950:
                    bot.editMessageText(mes_id,
                                        "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                               "обработка ролика</i>\n "
                                                                               "     ⏳ <i>Подготовка к отправке</i>\n "
                                                                               "     ⏳ <i>Отправка аудиофайла</i>")
                    Bot(955514245).sendMessage(url)
                    ditc.update({url: {"chat": chat_id, "mes_id": mes_id, "mes_id2": mes_id2}})
                    bot.editMessageText(mes_id,
                                        "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                               "обработка ролика</i>\n      ✅ "
                                                                               "<i>Подготовка к отправке</i>\n "
                                                                               "     ⏳ <i>Отправка аудиофайла</i>")
                    act_dict.update({str(chat_id) + str(mes_id): True})
                    fakeprocess(mes_id, artist, trackname, bot)
                    return
            inf = ydl.extract_info(query, force_generic_extractor=options.get('force_generic_extractor', False))
        if url:
            vid = inf.get('id')
        else:
            vid = inf.get('entries')[0].get('id')
            thumb = track.cover_art_url
        cover_art = utils.get_cover_art(thumb)
        delete_files.append(cover_art)
        act_dict.pop(str(chat_id) + str(mes_id))
        key = str(chat_id) + str(vid)
        act_dict.update({key: True})
        bot.editMessageText(mes_id,
                            "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                   "обработка ролика</i>\n      ✅ "
                                                                   "<i>Подготовка к отправке</i>\n "
                                                                   "     ⏳ <i>Отправка аудиофайла</i>")
        action(chat_id, key)
        ffmpeg = ffmpy.FFmpeg(
            inputs={logger.final_destination: None, cover_art: None, },
            outputs={output_path: '-loglevel quiet -hide_banner -y -map 0:0 -map 1:0 -id3v2_version 3 '
                                  '-metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" '
                                  '-af "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:'
                                  'detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:'
                                  'start_duration=1:start_threshold=-60dB:'
                                  'detection=peak,aformat=dblp,areverse"'}
        )
        try:
            ffmpeg.run()
        except Exception:
            delete_files.remove(cover_art)
            deleteFile(output_path)
            os.rename(f'{MYDIR}/{utils.TEMP_PATH}/{str(temp_file)}.mp3',
                      f'{MYDIR}/{utils.TEMP_PATH}/{artist} - {trackname}.{download_format}')
            deleteFile(cover_art)
            delete_files.remove(f'{MYDIR}/{utils.TEMP_PATH}/{str(temp_file)}.mp3')
            output_path = f'{MYDIR}/{utils.TEMP_PATH}/{artist} - {trackname}.{download_format}'
            delete_files.append(output_path)
        size = round(int(os.path.getsize(output_path)) / int(1048576), 2)
        aid = bot.sendAudio(output_path, size)
        act_dict.pop(key)
        bot.editMessageText(mes_id,
                            "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ✅ <i>Загрузка и "
                                                                   "обработка ролика</i>\n      ✅ "
                                                                   "<i>Подготовка к отправке</i>\n"
                                                                   "      ✅ <i>Отправка аудиофайла</i>")
        Timer(2, delmes, [bot, mes_id, mes_id2]).start()
        for file in delete_files:
            deleteFile(file)
            delete_files.remove(file)
        dbw = vedisdb.VDB(chat_id)
        queue = ast.literal_eval(dbw.get_current_state())
        queue.remove(cid)
        dbw.set_state(queue)
        data.addmusic(cid, aid[0], aid[1])
    except Exception:
        try:
            dbw = vedisdb.VDB(bot.chat_id)
            dbw.delete()
        except Exception:
            pass
        bot.editMessageText(mes_id,
                            "🎧<b>" + artist + " - " + trackname + "</b>\n\n      ❌ <i>Загрузка и "
                                                                   "обработка ролика</i>\n      ❌ "
                                                                   "<i>Подготовка к отправке</i>\n"
                                                                   "      ❌ <i>Отправка аудиофайла</i>")
        bot.sendMessage("Что-то пошло не так попробуйте немного позже")
        Timer(2, delmes, [bot, mes_id, mes_id2]).start()
        try:
            act_dict.pop(key)
        except Exception:
            pass
        try:
            act_dict.pop(str(chat_id) + str(mes_id))
        except Exception:
            pass
        try:
            for file in delete_files:
                deleteFile(file)
        except Exception:
            pass
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
