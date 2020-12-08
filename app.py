from flask import Flask, request
from bot import Bot
from threading import Thread, Timer
import vedisdb
import ast
import subprocess
import spotify
import download_task
from track import Track
import comands as com
import usersDB as dbase
import data as audioDB
import os
import sys
import data
import traceback

app = Flask(__name__)
keys_dct = {}


def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return execute


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        req = request.json
        main_func(req)
    return {"ok": True}


@thread
def main_func(r):
    try:
        try:
            text = r['message']['text']
        except KeyError:
            text = None
            try:
                calldata = r['callback_query']
            except KeyError:
                calldata = None
                try:
                    channel_post = r['channel_post']
                    if channel_post['chat']['id'] != -1001393645013:
                        channel_post = None
                except KeyError:
                    channel_post = None
        if text:
            chat_id = r["message"]["from"]['id']
            mes_id = r["message"]['message_id']
            dbase.add_user(chat_id, "ru", 1, 1)
            bot = Bot(chat_id)
            type_text(text, bot, mes_id)
        elif calldata:
            data = calldata.get("data")
            call_id = calldata.get("id")
            chat_id = calldata.get("from").get("id")
            bot = Bot(chat_id)
            bot.callback(data, calldata, call_id)
        elif channel_post:
            try:
                audio = channel_post['audio']
            except Exception:
                audio = None
            if audio:
                audio_id = audio['file_id']
                size = channel_post['caption'].split(":")[1].replace(" ", "").replace("Mb", "")
                aid = str(channel_post['reply_markup']['inline_keyboard'][0][0]['url']).replace("http://t.me"
                                                                                                "/Gozilla_bot?start=",
                                                                                                "")
                url = keys_dct.get(aid)
                inf = download_task.ditc.get(url)
                download_task.act_dict.pop(str(inf.get("chat")) + str(inf.get("mes_id")))
                bot = Bot(inf.get("chat"))
                bot.sendAudio(audio_id, size, True)
                Timer(2, download_task.delmes, [bot, inf.get("mes_id"), inf.get("mes_id2")]).start()
                dbw = vedisdb.VDB(inf.get("chat"))
                queue = ast.literal_eval(dbw.get_current_state())
                queue.remove(download_task.video_id(url))
                dbw.set_state(queue)
                audioDB.addmusic(download_task.video_id(url), audio_id, size)
            else:
                inf = str(channel_post['text']).split("+")
                keys_dct.update({inf[1]: inf[0]})
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def type_text(text, bot: Bot, mes_id2):
    try:
        if text in com.comands:
            com.comandor(bot.chat_id, text, "ru")
        elif download_task.video_id(text):
            vid = download_task.video_id(text)
            tg = data.findmusic(vid)
            if tg is not None:
                size = data.findsize(vid)
                bot.sendAudio(tg, size, True)
                Timer(2, bot.deleteMessage, [mes_id2]).start()
                return
            inf = download_task.namevid(vid)
            dbw = vedisdb.VDB(bot.chat_id)
            queue = dbw.get_current_state()
            if queue:
                queue = ast.literal_eval(queue)
                if str(vid) in queue:
                    bot.sendMessage("Этот трек уже скачиваеться!")
                    bot.deleteMessage(mes_id2)
                    return
                queue.append(vid)
                dbw.set_state(queue)
            else:
                dbw.set_state([vid])
            ids = bot.sendMessage("🎧<b>" + inf[0] + " - " + inf[1] + "</b>\n\n      ⏳ <i>Загрузка и "
                                                                      "обработка ролика 0%</i>\n      ⏳ "
                                                                      "<i>Подготовка к отправке</i>\n "
                                                                      "     ⏳ <i>Отправка аудиофайла</i>")
            download_task.download_task('0', 'mp3', 'downloads/', bot.chat_id, ids[0], inf[0], inf[1], url=text,
                                        thumb=inf[2], mes_id2=mes_id2)
        else:
            track_list = []
            search_query = text
            need = spotify.search(search_query)
            try:
                need += spotify.search(search_query, 49)
                need += spotify.search(search_query, 99)
            except TypeError:
                pass
            try:
                track = [[Track(item)] for item in need]
            except TypeError:
                bot.deleteMessage(mes_id2)
                bot.sendMessage("По запросу \"<i>" + text + "</i>\" ничего не найдено")
                return
            for x in range(len(need)):
                track_list.append([])
            num = 0
            for trach in track:
                if len(trach[0].artist_names) > 1:
                    if "feat" in trach[0].name:
                        art = str(trach[0].artist_names[0])
                    else:
                        art = str(trach[0].artist_names[0])
                        for name in trach[0].artist_names[1:]:
                            art += ", " + str(name)
                else:
                    art = str(trach[0].artist_names[0])
                track_list[num].append(
                    {'text': art + ' - ' + trach[0].name, 'callback_data': trach[0].url})
                num += 1
            if len(track_list) > 8:
                pag_nums = ((len(track_list)) // 8) + 1
                track_list.append([{"text": 1, "callback_data": "a"}, {"text": "▶️", "callback_data": "forward"}])
                track_list.append([{"text": "Удалить это сообщение", "callback_data": "del"}])
                track_list.append(str(1) + "+" + str(pag_nums))
                send = bot.init_inline_keyboard(track_list[:8] + [track_list[:-2][-1]] + [track_list[:-1][-1]],
                                                'Результат поиска по запросу - "' + str(search_query) + '"'
                                                                                                        '\n'
                                                                                                        '--------------------------------------------\n'
                                                                                                        'Страница 1 из ' + str(
                                                    pag_nums))
                bot.deleteMessage(mes_id2)
                dbw = vedisdb.VDB(str(send[0]) + str(bot.chat_id))
                dbw.set_state(track_list)
            else:
                bot.init_inline_keyboard(track_list, 'Результат поиска по запросу - "' + str(search_query) + '"'
                                                                                                             '\n'
                                                                                                             '--------------------------------------------\n'
                                                                                                             'Страница 1 из 1')
                bot.deleteMessage(mes_id2)
    except Exception:

        try:
            dbw = vedisdb.VDB(bot.chat_id)
            queue = ast.literal_eval(dbw.get_current_state())
            queue.remove(vid)
            dbw.set_state(queue)
        except Exception:
            pass
        bot.editMessageText(ids[0],
                            "🎧<b>" + inf[0] + " - " + inf[1] + "</b>\n\n      ❌ <i>Загрузка и "
                                                                "обработка ролика</i>\n      ❌ "
                                                                "<i>Подготовка к отправке</i>\n"
                                                                "      ❌ <i>Отправка аудиофайла</i>")
        bot.sendMessage("Что-то пошло не так попробуйте немного позже")
        Timer(2, download_task.delmes, [bot, ids[0], mes_id2]).start()
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    subprocess.Popen("python3 agent.py", shell=True)
    app.run(host='0.0.0.0', port=port)
