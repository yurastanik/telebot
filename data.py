import psycopg2
from bot import Bot
import traceback
import sys

bot = Bot(None)


def conect():
    try:
        connect = psycopg2.connect(database='d5qra7lfob5dvs', user='bsnjlfmyrjcddb',
                                   password='d841dd57c541777478a380656687f3ed2541f96e39cab1ae4584bf6dd504aeb4',
                                   host='ec2-54-75-235-28.eu-west-1.compute.amazonaws.com', port='5432')
        cursor = connect.cursor()
        return [connect, cursor]
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        bot.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def addmusic(ytid, tgid, size):
    try:
        db = conect()
        db[1].execute('INSERT INTO "audio" VALUES (%s, %s, %s)', (ytid, tgid, size))
        db[0].commit()
        return True
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        bot.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        return False


def findsize(ytid):
    try:
        stmt = 'SELECT "size" FROM "audio" WHERE ytid = (%s)'
        args = (ytid,)
        db = conect()
        db[1].execute(stmt, args)
        p = db[1].fetchone()
        b = p[0]
        db[1].close()
        db[0].commit()
        return b
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        bot.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        return None


def findmusic(ytid):
    try:
        stmt = 'SELECT "tgid" FROM "audio" WHERE ytid = (%s)'
        args = (ytid,)
        db = conect()
        db[1].execute(stmt, args)
        p = db[1].fetchone()
        b = p[0]
        db[1].close()
        db[0].commit()
        db[0].close()
        return b
    except Exception as e:
        if str(e) == "'NoneType' object is not subscriptable":
            return None
        else:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            bot.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
            conect()
            return None


def count():
    try:
        db = conect()
        db[1].execute('SELECT count(*) from "audio"')
        db[0].commit()
        return db[1].fetchone()
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        bot.sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return False
