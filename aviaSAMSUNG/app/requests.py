from flask import Blueprint, request
from app.db import auth, get_user_data_by_phone, add_new_user, update_data, check_tickets, check_dtickets
from app.SMS import checkSMS, sendSMS

module = Blueprint('main', __name__, url_prefix='/')


@module.get("/")
def index():
    print('HE!!O')


@module.post("/login")
def login():
    data = request.get_json()
    print(data["phone"])
    if auth(data["phone"]) is None:# or: (not sendSMS(data["phone"])):
        return {
            "status" : "Failed"
        }

    # if not sendSMS(data["phone"]):
    #     return {
    #         "status" :"Error"
    #     }
    
    return {
        "status" : "Successfully"
    }

@module.post("/registration")
def registration():
    data = request.get_json()
    if auth(data["phone"]):
        return {
            "status" : "failed",
            "message" : "Пользователь с таким номером телефона уже существует"
        }
    else:
        add_new_user(data["phone"], data["password"])
        # if not sendSMS(data["phone"]):
        #     return {
        #         "status" :"Error"
        #     }
    
        return {
            "status" : "Successfully"
        }

@module.post("/code")
def get_code():
    data = request.get_json()
    if checkSMS(data["phone"], data["code"]):
        login = get_user_data_by_phone(data["phone"])
        return {
            "status" : "Successfully",
            "message" : "Добро пожаловать, " + login[0],
            "user_data" : login
        }
    
    return {
        "status" : "failed",
        "message" : "Неверный код",
        "user_data" : "empty"
    }
        
@module.post("/tickets")
def tickets():
    data = request.get_json()
    fromWhere = data["fromWhere"]
    toWhere = data["toWhere"]
    date = data["date"]
    ticketsF = [1, 1, 1, "any", 1]
    filters = data["filters"].split("_")
    print(date)
    print(filters)
    for i in range(len(filters)):
        if filters[i] == "null": continue
        if i == 3: ticketsF[i] = filters[i]
        else: ticketsF[i] = int(filters[i])

    print(ticketsF)
    res = check_tickets(fromWhere, toWhere, date, ticketsF[0], ticketsF[1], ticketsF[2], ticketsF[3], ticketsF[4])

    if res == None:
        return {
            "status" : "failed",
            "message" : "Нет билетов",
        }
    
    else:
        return {
            "status" : "Successfully",
            "message" : res
        }

    
@module.post("/dtickets")
def dtickets():
    data = request.get_json()
    ids = data["id"].split()
    print(ids)
    res = ''
    for i in range(len(ids)):
        res += check_dtickets(ids[i]) + "SPLITTING"

    print(res.split("SPLITTING"))
    

    if res == None:
        return {
            "status" : "failed",
            "message" : "Пуста"
        }
    
    else:
        print(res)
        return {
            "status" : "Successfully",
            "message" : res
        }

@module.post("/update")
def update():
    data = request.get_json()
    phone = data["phone"]
    name = data["name"]
    surname = data["surname"]
    passS = data["passS"]
    passN = data["passN"]

    if update_data(phone, name, surname, passS, passN):
        return {
            "status" : "Succesfully",
            "message" : "Updated"
        }
    
    return {
        "status" : "Failed",
        "message" : "Not Updated"
    }

@module.post("/logout")
def logout():
    return {
        "status" : "accepted",
        "message" : "До свидания!"
    }