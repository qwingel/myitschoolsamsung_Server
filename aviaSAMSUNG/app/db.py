import sqlite3
from datetime import date

today = date.today()
tm = today.month
td = today.day

db = sqlite3.connect('skyline.db', 10.0, check_same_thread=False)

def auth(phone: str):
    res = db.execute(
        """SELECT * FROM users WHERE phone = ?""",
        (phone,)
    )

    if res.fetchone() is None:
        return None
    
    return phone

def create_empty_fields():
    db.execute(
        """INSERT INTO users_data
        (login, passport_series, passport_number, surname, name, birthday)
        VALUES
        (?, ?, ?, ?, ?, ?)""", ('Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто')
    )
    db.commit()

def add_new_user(phone:str, password:str):
    db.execute(
        """INSERT INTO users 
        (phone, password)
        VALUES
        (?, ?)""", (phone, password)
    )
    db.commit()
    create_empty_fields()
    
def get_user_data_by_phone(phone:str):
    data = ['Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто', 'Пусто']

    res1 = db.execute(
        """SELECT id FROM users WHERE phone = ?""",
        (phone,)
    )

    id = res1.fetchone()[0]

    if phone == 'failed_loginconn':
        return data
    
    else:
        res = db.execute(
            """SELECT * FROM users_data WHERE id = ?""",
            (id,)
        )

        res2 = db.execute(
            """SELECT password FROM users WHERE id = ?""",
            (id,)
        )

        ress = res.fetchone()
        password = res2.fetchone()[0]
        passport_series = ress[2]
        passport_number = ress[3]
        surname = ress[4]
        name = ress[5]
        birthday = ress[6]

        return (password + ' ' + name + ' ' + surname + ' ' + \
            passport_series + ' ' + passport_number + ' ' + \
            birthday)

def check_dtickets(id:str):
    res = db.execute(
    """SELECT * FROM tickets WHERE id = ?""", (id,)
    )

    ress = res.fetchall()
    print(ress,'id == ' + id)
    if ress is None:
        return ''
    
    ticket_str = str(ress)[2:-2].replace("), (", "SPLITTING")
    print(ticket_str)
    return ticket_str

def update_data(phone:str, name:str, surname:str, passS:str, passN:str):
    res = db.execute(
        """SELECT id FROM users WHERE phone = ?""", (phone, )
    )
    id = res.fetchone()[0]
    print(id)
    res1 = db.execute(
        """UPDATE users_data SET name = ?, surname = ?, passport_series = ?, passport_number = ? WHERE id = ?""", (name, surname, passS, passN, id, )
    )
    db.commit()
    if res1 is None:
        return False
    
    return True

def check_tickets(fromWhere:str, toWhere:str, date:str, ticketsCount:int, ticketsWithChild:int, ticketsWithKids:int, ticketsClass:str, ticketsBaggage:int):
    print(ticketsCount, ticketsWithChild, ticketsWithKids, ticketsClass)
    if  date == "*":
        res = db.execute(
        """SELECT * FROM tickets WHERE fromWhere = ? AND toWhere = ? \
            AND (isChild = ? OR isChild = 1) AND (isKid = ? OR isKid = 1) AND (class = ? OR class = 'any') \
            AND Baggage = ? AND ticketsCount >= ?""", (fromWhere, toWhere, ticketsWithChild, ticketsWithKids, ticketsClass, ticketsBaggage, ticketsCount,)
        )
    
    def getMonth(i):
        months = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЯ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК']
        if isinstance(i, int):
            return months[i]
        
        elif isinstance(i, str):
            return months.index(i[1:-1]) + 1


    if date != '*':
        date1, month, year = date.split('.')
        month1 = getMonth(int(month))
        print(date1, month1)
        res = db.execute(
        """SELECT * FROM tickets WHERE fromWhere = ? AND toWhere = ? \
            AND ((Month = ? AND Date > ?) OR (Month != ?)) \
            AND (isChild = ? OR isChild = 1) AND (isKid = ? OR isKid = 1) AND (class = ? OR class = 'any') \
            AND Baggage = ? AND ticketsCount >= ?""", (fromWhere, toWhere, month1, date1, month1, ticketsWithChild, ticketsWithKids, ticketsClass, ticketsBaggage, ticketsCount,)
        )

    ress = res.fetchall()
    print(ress, res)
    if ress is None:
        return None
    
    ticket_list = str(ress)[2:-2].split("), (")
    ticket_str = str(ress)[2:-2].replace("), (", "SPLITTING")

    def theNearestTicket(a:list) -> str:
        if date != '*':
            day, month, year = map(int, date.split('.'))

        else:
            day, month = td, tm

        b = []
        ind = '0'
        for i in range(len(a)):
            c = a[i].split(', ')
            nowMonth = getMonth(c[3])
            if nowMonth == month:
                if int(c[4]) >= day:
                    ind = c[0]
                    b.append([int(c[4]), getMonth(c[3]), ind])

            if nowMonth > month:
                ind = c[0]
                b.append([int(c[4]), getMonth(c[3]), ind])

        b.sort(key=lambda x: (x[1], x[0]))
        res = b[0][2]

        print(b, 'id = ' + res)

        for i in range(len(a)):
            c = a[i].split(', ')
            print(c, c[0] == res)
            if c[0] == res:
                print(a[i])
                return a[i] + "SPLITTING"
            
        return '0'
            
    def theBestPrice(a:list) -> str:
        minPrice = 10 ** 20
        ids = -1

        for i in range(len(a)):
            b = a[i].split(", ")
            if int(b[-1]) < minPrice:
                ids = int(b[0])
                minPrice = int(b[-1])

        for i in range(len(a)):
            b = a[i].split(", ")
            if ids == int(b[0]):
                return a[i] + "SPLITTING"

        return '0'
    
    if ticket_list != '':
        bestPriceTicket = theBestPrice(ticket_list)
        nearestTicket = theNearestTicket(ticket_list)

    result = ticket_str.replace(bestPriceTicket, '')
    result = result.replace(nearestTicket, '')
    

    # print(bestPriceTicket + ticket_str.replace(bestPriceTicket, ''))
    return nearestTicket + bestPriceTicket + result


update_data('79965909961', 'Артём' , 'Попов', '8711', '881231')