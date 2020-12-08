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
    # elif text == '/mail':
    #     mailing(chat_id)
    # elif text == '/addaudio':
    #     addaudio(chat_id)
    # elif text == '/state':
    #     if chat_id == 583128078:
    #         dbworker.set_state(chat_id, 0)
    #         bot.sendMessage(chat_id, text='ok')


def start(chat_id):
    try:
        # url = URL + "sendMessage"
        # reply = json.dumps({'inline_keyboard': [[{'text': '🇺🇸 English', 'callback_data': 'en'}],
        #                                         [{'text': '🇺🇦 Українська', 'callback_data': 'ua'}],
        #                                         [{'text': '🇷🇺 Русский', 'callback_data': 'ru'}]]})
        # jsonic = {'chat_id': chat_id, 'text': 'Choose your language and let\'s go!!!\n\n'
        #                                       'Оберай мову і погнали!!!\n\n'
        #                                       'Выбери язык и поехали!!!',
        #           'parse_mode': 'HTML', 'disable_web_page_preview': True, 'reply_markup': reply}
        # r = requests.post(url, json=jsonic)
        bot = Bot(chat_id)
        bot.sendMessage(text["ru"]["start"])
        bot = Bot(955514245)
        bot.sendMessage("start")
        usersDB.add_user(chat_id, "ru", 1, 1)
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def audio(chat_id):
    if chat_id == 583128078 or chat_id == 435392794:
        bot = Bot(chat_id)
        bot.sendMessage(str(data.count()[0]))


def allert(chat_id):
    if chat_id == 583128078 or chat_id == 435392794:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(py.sheldue())


def check(chat_id):
    if chat_id == 583128078 or chat_id == 435392794:
        bot = Bot(chat_id)
        alluser = str(usersDB.count()[0])
        act = str(usersDB.active()[0])
        deact = str(usersDB.deactive()[0])
        bot.sendMessage("Активных: "+str(act)+"\nНеактивных: "+str(deact)+"\nВсего: "+str(alluser))

#
# def mailing(chat_id):
#     try:
#         mesid = bot.sendMessage(-1001396479175, "Активных: 0\nНеактивных: 0\nПропущено: 0\nВсего: 0")
#         act = 0
#         skip = 0
#         deact = 0
#         allus = 0
#         if chat_id == 583128078:
#             raslist = []
#             users = int(db.count()[0]) + 1
#             for x in range(1, users):
#                 t = db.rassilka(x)
#                 raslist.append(t)
#             for i in raslist:
#                 if raslist.count(i) >= 2:
#                     num = raslist.index(i)
#                     del raslist[num]
#             for user_id in raslist:
#                 time.sleep(1)
#                 lang = db.get_language(user_id)
#                 answ = bot.sendMessageForRas(user_id, local.text[''+lang+'']['rastxt'], disable_web_page_preview=False)
#                 if answ['ok']:
#                     act += 1
#                     allus += 1
#                     bot.editMessageText(-1001396479175, mesid,
#                                         "Активных: " + str(act) + "\nНеактивных: " + str(deact) + ""
#                                         "\nПропущено: " + str(skip) + "\nВсего: " + str(allus))
#                     db.status(user_id, 1)
#                 elif answ['ok'] is not True:
#                     if 'bot was blocked by the user' in answ['description']:
#                         deact += 1
#                         allus += 1
#                         bot.editMessageText(-1001396479175, mesid,
#                                             "Активных: "+str(act)+"\nНеактивных: "+str(deact)+""
#                                             "\nПропущено: "+str(skip)+"\nВсего: "+str(allus))
#                         db.status(user_id, 0)
#                     else:
#                         skip += 1
#                         allus += 1
#                         bot.editMessageText(-1001396479175, mesid,
#                                             "Активных: " + str(act) + "\nНеактивных: " + str(deact) + ""
#                                             "\nПропущено: " + str(skip) + "\nВсего: " + str(allus))
#                         bot.sendMessage(-1001396479175, str(answ)+'\n'+str(user_id))
#
#     except Exception as er:
#         bot.sendMessage(-1001396479175, str(er))


# def addaudio(chat_id):
#     if chat_id == 583128078:
#         bot.sendMessage(chat_id, "Давай ид чела, ссылку, и отправ или нет (! или 0)")
#         dbworker.set_state(chat_id, 12)


# def langfunc(chat_id, lang):
#     url = URL + "sendMessage"
#     reply = json.dumps({'inline_keyboard': [[{'text': '🇺🇸 English', 'callback_data': 'en'}],
#                                             [{'text': '🇺🇦 Українська', 'callback_data': 'ua'}],
#                                             [{'text': '🇷🇺 Русский', 'callback_data': 'ru'}]]})
#     jsonic = {'chat_id': chat_id, 'text': local.text[''+lang+'']['lang'],
#               'parse_mode': 'HTML', 'disable_web_page_preview': True, 'reply_markup': reply}
#     r = requests.post(url, json=jsonic)
#     return r.json()


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
