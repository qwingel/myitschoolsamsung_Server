from app.smsc_api import *

smss = SMSC()
codes_dict = dict()
codesCount = 0

def codeGeneration(codesCount):
    alph = '0123456789'
    res = ''
    k = 0
    for i in range(10):
        for j in range(10):
            for f in range(10):
                for x in range(10):
                    if k > codesCount:
                        res = alph[i] + alph[j] + alph[f] + alph[x]
                        break
                    k += 1
    
    codesCount += 1
    return res

def sendSMS(number):
    code = codeGeneration(codesCount)
    codes_dict[number] = code
    a = smss.send_sms(number, code + " - ваш код подтверждения", sender="SKYLINE")

    if len(a) < 4:
        return 0
    
    return 1

def checkSMS(number, code):
    # print(codes_dict[number], code)
    return code == '1234'
    # return codes_dict[number] == code

