import sqlite3
import uuid
import datetime
from planner.__main__ import PATH
from PyQt5.QtCore import QDateTime

connection = None


def update_entry(rem_id, name=None, description=None, time=None, done=None):
    global connection
    cur = connection.cursor()

    if rem_id.__class__ == uuid.UUID:
        rem_id = str(rem_id)
    data = get_entry(rem_id)
    if len(data) == 0:
        raise Exception('Reminder not found')
    query = 'update entries set\n'
    if name is not None:
        query += 'name = \'' + str(name) + '\',\n'
    if description is not None:
        query += 'description = \'' + str(description) + '\',\n'
    if time is not None:
        query += 'time = ' + str(time) + ',\n'
    if done is not None:
        query += 'done = \'' + str(done) + '\'\n'
    if query[-2] == ',':
        query = query[:-2] + '\n'
    query += 'where id == ?'
    cur.execute(query, (rem_id,))
    connection.commit()


def add_entry(name, time, description=None):
    entry_id = uuid.uuid4()
    global connection
    cur = connection.cursor()
    cur.execute('insert into entries values(?, ?, ?, ?, ?)', (str(entry_id), name, description, time, False))
    connection.commit()
    return entry_id


def get_entry(rem_id):
    global connection
    if rem_id.__class__ == uuid.UUID:
        rem_id = str(rem_id)
    cur = connection.cursor()
    result = cur.execute('select id, name, description, time, done from entries where id == ?', (rem_id,)).fetchone()
    return result


def get_entries_by_date(date):
    """ аргумент date - объект типа QDate """
    global connection
    cur = connection.cursor()
    date = datetime.datetime.fromtimestamp(QDateTime(date).toSecsSinceEpoch()).date()
    result = cur.execute('select id, name, description, time, done from entries where time >= ? and time < ?',
                         (datetime.datetime.combine(date, time=datetime.time(0)).timestamp(),
                          datetime.datetime.combine(date=date + datetime.timedelta(days=1),
                                                    time=datetime.time(0)).timestamp())).fetchall()
    return result


def get_all_entries(group_by_status=False):
    global connection
    cur = connection.cursor()

    query = 'select id, name, description, time, done from entries\n'
    if group_by_status:
        query += 'order by done, time\n'
    else:
        query += 'order by time\n'

    result = cur.execute(query).fetchall()
    return result


def connect():
    global connection
    connection = sqlite3.connect(PATH + '\\planner.db')
