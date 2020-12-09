import requests
import json
import sys
import traceback
from threading import Thread, Timer
import vedisdb
import ast
import spotify
from localization import text
import asyncio

Token = '1233508198:AAGbqnCTflzBs59hrRkDPO62rRnosV_qfDQ'

URL = "https://api.telegram.org/bot{}/".format(Token)


def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return execute


def answerCallbackQuery(call_id, text, show_alert=True):
    url = URL + "answerCallbackQuery"
    data = {'callback_query_id': call_id, 'text': text, 'show_alert': show_alert}
    requests.post(url, data=data).json()


class Bot:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.error_id = channel_id
        if chat_id is None:
            self.chat_id = self.error_id

    def init_inline_keyboard(self, buttons, text):
        reply = json.dumps({'inline_keyboard': buttons})
        inf = self.sendMessage(text=text, reply=reply)
        return inf

    def deleteMessage(self, mes_id):
        try:
            url = URL + "deleteMessage"
            jsondata = {'chat_id': self.chat_id, 'message_id': mes_id}
            r = requests.post(url, json=jsondata)
            return r.json()
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            self.chat_id = self.error_id
            self.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))

    def sendChatAction(self):
        try:
            url = URL + "sendChatAction"
            jsondata = {'chat_id': self.chat_id, 'action': "upload_audio"}
            r = requests.post(url, json=jsondata)
            return r.json()
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            self.chat_id = self.error_id
            self.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))

    def editMessageText(self, mes_id, text, reply=None):
        try:
            url = URL + "editMessageText"
            jsondata = {'chat_id': self.chat_id, 'message_id': mes_id, 'text': text, 'parse_mode': 'HTML',
                        'disable_web_page_preview': True}
            if reply is not None:
                jsondata.update({'reply_markup': {'inline_keyboard': reply}})
            r = requests.post(url, json=jsondata).json()
            try:
                text = r['result']['text']
            except KeyError:
                text = r
            return text
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            self.chat_id = self.error_id
            self.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))

    def sendMessage(self, text='Smth wrong!', parseMode="HTML", disable_web_page_preview=True, reply=None):
        url = URL + "sendMessage"
        jsondata = {'chat_id': self.chat_id, 'text': text, 'parse_mode': parseMode,
                    'disable_web_page_preview': disable_web_page_preview}
        if reply:
            jsondata.update({'reply_markup': reply})
        r = requests.post(url, json=jsondata).json()
        try:
            id = r['result']['message_id']
            text = r['result']['text']
        except KeyError:
            id = None
            text = None
        return [id, text]

    def sendAudio(self, file, size, tgid=False):
        url = URL + "sendAudio"
        try:
            if tgid:
                data = {'audio': file, 'chat_id': self.chat_id, 'caption': "your caption",
                        'parse_mode': 'HTML'}
                requests.post(url, data=data).json()
            else:
                with open(str(file), 'rb') as f:
                    data = {'chat_id': self.chat_id, 'caption': "your caption",
                            'parse_mode': 'HTML'}
                    files = {'audio': f}
                    r = requests.post(url, files=files, data=data).json()
                    f.close()
                return [r['result']['audio']['file_id'], size]
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            self.sendMessage(text="Попробуйте ещё раз")
            self.chat_id = self.error_id
            self.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]) + "\n" + r)
            return False


    def editMessageReplyMarkup(self, mes_id, new_buttons):
        try:
            reply = json.dumps({'inline_keyboard': new_buttons})
            jsonic1 = {'chat_id': self.chat_id, 'message_id': mes_id, 'reply_markup': reply}
            r = requests.post(URL + "editMessageReplyMarkup", json=jsonic1)
            return r.json()
        except Exception:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            self.chat_id = self.error_id
            self.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))

    def callback(self, data, callda, call_id):
        try:
            if data == "en" or data == "ua" or data == "ru":
                from usersDB import add_user
                add_user(self.chat_id, data, 1, 1)
                self.sendMessage(text["ru"]["start"])
            elif data == "del":
                mes_id = callda.get("message").get("message_id")
                self.deleteMessage(mes_id)
                dbw = vedisdb.VDB(str(mes_id) + str(self.chat_id))
                dbw.delete()
            elif data == "forward":
                mes_id = callda.get("message").get("message_id")
                dbw = vedisdb.VDB(str(mes_id) + str(self.chat_id))
                dt = dbw.get_current_state()
                if not dt:
                    answerCallbackQuery(call_id, "Время истекло, повторите запрос ещё раз")
                    return
                new_trklist = ast.literal_eval(dt)
                cur_num, all_num = new_trklist[-1].split("+")
                from_num = 8 * int(cur_num)
                next_num = int(from_num) + 8
                if int(cur_num) + 1 == int(all_num):
                    new_trklist[len(new_trklist) - 3] = [{"text": "◀️", "callback_data": "back"},
                                                         {"text": int(cur_num) + 1, "callback_data": "a"}]
                    next_num = len(new_trklist) - 3
                else:
                    new_trklist[len(new_trklist) - 3] = [{"text": "◀️", "callback_data": "back"},
                                                         {"text": int(cur_num) + 1, "callback_data": "a"},
                                                         {"text": "▶️", "callback_data": "forward"}]
                new_trklist[-1] = str((int(cur_num) + 1)) + "+" + str(all_num)
                self.editMessageText(mes_id, 'Результат поиска по запросу - "' + str(
                    callda.get('message').get('text').split("\"")[1]) + '"'
                                                                        '\n'
                                                                        '--------------------------------------------\n'
                                                                        'Страница ' + str(int(cur_num) + 1) + ' из ' +
                                     str(all_num),
                                     new_trklist[from_num:next_num] + [new_trklist[:-2][-1]] + [new_trklist[:-1][-1]])
                dbw.set_state(new_trklist)
            elif data == "back":
                mes_id = callda.get("message").get("message_id")
                dbw = vedisdb.VDB(str(mes_id) + str(self.chat_id))
                dt = dbw.get_current_state()
                if not dt:
                    answerCallbackQuery(call_id, "Время истекло, повторите запрос ещё раз")
                    return
                new_trklist = ast.literal_eval(dt)
                cur_num, all_num = new_trklist[-1].split("+")
                from_num = 8 * (int(cur_num) - 2)
                next_num = int(from_num) + 8
                if int(cur_num) == 2:
                    new_trklist[len(new_trklist) - 3] = [{"text": int(cur_num) - 1, "callback_data": "a"},
                                                         {"text": "▶️", "callback_data": "forward"}]
                else:
                    new_trklist[len(new_trklist) - 3] = [{"text": "◀️", "callback_data": "back"},
                                                         {"text": int(cur_num) - 1, "callback_data": "a"},
                                                         {"text": "▶️", "callback_data": "forward"}]
                new_trklist[-1] = str((int(cur_num) - 1)) + "+" + str(all_num)
                self.editMessageText(mes_id, 'Результат поиска по запросу - "' + str(
                    callda.get('message').get('text').split("\"")[1]) + '"'
                                                                        '\n'
                                                                        '--------------------------------------------\n'
                                                                        'Страница ' + str(
                    int(cur_num) - 1) + ' из ' + str(
                    all_num), new_trklist[from_num:next_num] + [new_trklist[:-2][-1]] + [new_trklist[:-1][-1]])
                dbw.set_state(new_trklist)
            elif data != "a":
                track = spotify.link(data)
                track_info = track[0]
                import data as db
                tg = db.findmusic(track_info.id)
                if tg is not None:
                    size = db.findsize(track_info.id)
                    self.sendAudio(tg, size, True)
                    return
                dbw = vedisdb.VDB(self.chat_id)
                queue = dbw.get_current_state()
                if queue:
                    queue = ast.literal_eval(queue)
                    if str(track_info.id) in queue:
                        answerCallbackQuery(call_id, "Этот трек уже скачиваеться!")
                        return
                    queue.append(track_info.id)
                    dbw.set_state(queue)
                else:
                    dbw.set_state([track_info.id])
                track_name = str(track_info.name)
                if len(track_info.artist_names) > 1:
                    if "feat" not in track_info.name:
                        track_name += " (feat. "
                        for name in track_info.artist_names[1:]:
                            track_name += str(name) + ", "
                        track_name += ")"
                        track_name = track_name.replace(", )", ")")
                art = str(track_info.artist_names[0])
                ids = self.sendMessage("🎧<b>" + art + " - " + track_name + "</b>\n\n      ⏳ <i>Загрузка и "
                                                                            "обработка ролика 0%</i>\n      ⏳ "
                                                                            "<i>Подготовка к отправке</i>\n "
                                                                            "     ⏳ <i>Отправка аудиофайла</i>")
                from download_task import download_task
                download_task('0', 'mp3', 'downloads/', self.chat_id, ids[0], art, track_name, track_info)
        except Exception:
            try:
                self.editMessageText(ids[0],
                                     "🎧<b>" + art + " - " + track_name + "</b>\n\n      ❌ <i>Загрузка и "
                                                                          "обработка ролика</i>\n      ❌ "
                                                                          "<i>Подготовка к отправке</i>\n"
                                                                          "      ❌ <i>Отправка аудиофайла</i>")
                Timer(2, download_task.delmes, [self, ids[0], None]).start()
            except Exception:
                pass
            self.sendMessage("Что-то пошло не так попробуйте немного позже")
            try:
                dbw = vedisdb.VDB(self.chat_id)
                queue = ast.literal_eval(dbw.get_current_state())
                queue.remove(track_info.id)
                dbw.set_state(queue)
            except Exception:
                pass
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
            dbw = vedisdb.VDB(self.chat_id)
            dbw.delete()

