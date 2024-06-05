import sqlite3
import random

db = sqlite3.connect('skyline.db', 10.0, check_same_thread=False)

months = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЯ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК']
day = [i for i in range(1, 30)]
city = ['Moscow', 'SPB', 'Sochi', 'Sktr']
hour = [str(i) for i in range(10, 23)]
minute = [str(i) for i in range(10, 60)]


def getRandom(list_Random:list):
    return list_Random[random.randint(0, len(list_Random) - 1)]

def Generate():
    x = getRandom(hour)
    y = getRandom(minute)
    x1, y1 = str(int(x) + 2), y
    res = db.execute(
        """INSERT INTO tickets
        (fromWhere, toWhere, Month, Date, timeOut, timeTo, isChild, isKid, class, Baggage, ticketsCount, price)
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (getRandom(city), getRandom(city), getRandom(months), getRandom(day), x + ':' + y, \
        x1 + ':' + y1, 1, 1, 'any', 1, 70, random.randint(1790, 3590))
    )
    db.commit()

def Find():
    res = db.execute(
        """SELECT * FROM tickets 
        WHERE fromWhere = ? AND toWhere = ?""", ('Sktr', 'Moscow')
    )

    return res.fetchall()

def Delete():
    res = db.execute(
        """DELETE FROM tickets WHERE timeOut > timeTo"""
    )
    db.commit()


# print(Find())