# -*- coding: utf-8 -*-

import psycopg2
from bot import Bot
import sys
import traceback


def conect():
    connection = psycopg2.connect(database='databsname', user='databsuser',
                                  password='databspass',
                                  host='databshos', port='port')
    cursor = connection.cursor()
    return [connection, cursor]


bot = Bot(None)


def add_user(id, language, status, log):
    try:
        db = conect()
        db[1].execute('INSERT INTO "usersdb" VALUES (%s, %s, %s, %s)', (id, language, status, log))
        db[0].commit()
        return True, True
    except psycopg2.errors.UniqueViolation:
        db = conect()
        db[1].execute("ROLLBACK")
        db[0].commit()
        db[1].execute('UPDATE "usersdb" SET "language" = (%s) WHERE id = (%s)', (language, id))
        db[0].commit()
        return True, False
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return False, False


def status(id, status):
    try:
        db = conect()
        db[1].execute('UPDATE "usersdb" SET "status" = (%s) WHERE id = (%s)', (status, id))
        db[0].commit()
        return True
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return


def editlog(id, log):
    try:
        db = conect()
        db[1].execute('UPDATE "usersdb" SET "log" = (%s) WHERE id = (%s)', (log, id))
        db[0].commit()
        return True
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return


def rassilka(numb):
    try:
        stmt = """SELECT "id" FROM (SELECT ROW_NUMBER () OVER (ORDER BY status) AS RowNum, * FROM public.usersdb) sub WHERE RowNum = (%s)"""
        args = (numb,)
        db = conect()
        db[1].execute(stmt, args)
        p = db[1].fetchone()
        b = p[0]
        return b
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return '583128078'


def getlog(id):
    try:
        stmt = """SELECT "log" FROM public.usersdb WHERE id = (%s)"""
        args = (id,)
        db = conect()
        db[1].execute(stmt, args)
        p = db[1].fetchone()
        b = p[0]
        return b
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return '2'


def active():
    try:
        db = conect()
        db[1].execute('SELECT count(*) from "usersdb" WHERE "status" = 1')
        db[0].commit()
        return db[1].fetchone()
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return False


def delete(chat_id):
    try:
        db = conect()
        db[1].execute('DELETE FROM public.usersdb * WHERE id = %d' % chat_id)
        db[0].commit()
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return False


def deactive():
    try:
        db = conect()
        db[1].execute('SELECT count(*) from "usersdb" WHERE "status" = 0')
        db[0].commit()
        return db[1].fetchone()
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return False


def count():
    try:
        db = conect()
        db[1].execute('SELECT count(*) from "usersdb"')
        db[0].commit()
        return db[1].fetchone()
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
        conect()
        return False


def get_language(id):
    try:
        db = conect()
        stmt = """SELECT "language" FROM public.usersdb WHERE id = (%s)"""
        args = (id,)
        db[1].execute(stmt, args)
        p = db[1].fetchone()
        b = p[0]
        db[1].close()
        db[0].commit()
        db[0].close()
        return b
    except Exception as e:
        if "'NoneType' object is not subscriptable" in str(e):
            return "en"
        else:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))
            conect()
            return "en"
