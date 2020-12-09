import usersDB
import data
from bot import Bot
import sys
import traceback
import py
from localization import text
from threading import Thread
import asyncio

comands = ['/start', '/help', '/users', '/audio', '/alert']


def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute


Token = '1233508198:AAGbqnCTflzBs59hrRkDPO62rRnosV_qfDQ'

URL = "https://api.telegram.org/bot{}/".format(Token)


@thread
def comandor(chat_id, text, lang):
    if text == '/start':
        start(chat_id)
    elif text == '/help':
        helpme(chat_id)
    elif text == '/audio':
        audio(chat_id)
    elif text == '/users':
        check(chat_id)
    elif text == '/alert':
        allert(chat_id)


def start(chat_id):
    try:
        bot = Bot(chat_id)
        bot.sendMessage(text["ru"]["start"])
        bot = Bot(955514245)
        bot.sendMessage("start")
        usersDB.add_user(chat_id, "ru", 1, 1)
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def check(chat_id):
    if chat_id == my_id:
        bot = Bot(chat_id)
        alluser = str(usersDB.count()[0])
        act = str(usersDB.active()[0])
        deact = str(usersDB.deactive()[0])
        bot.sendMessage("Активных: "+str(act)+"\nНеактивных: "+str(deact)+"\nВсего: "+str(alluser))
  

def helpme(chat_id):
    try:
        bot = Bot(chat_id)
        link = "<a href=\"https://www.youtube.com/\" >YouTube</a>"
        bot.sendMessage(text="Этот бот может скачать твой любимый трек или видео с "+link+". Тебе лишь нужно отправить "
                             "название трека или ссылку с "+link+", немножко подождать и бот отправит тебе аудио файл "
                                                                 "и удалит ненужные сообщения. Вот и всё, приятного "
                                                                 "пользования😉.")
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
