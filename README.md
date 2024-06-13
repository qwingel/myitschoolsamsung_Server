# SkyLine
**Серверная часть приложения SkyLine**

## Запуск
main.py:
```python
import waitress
from app import yourapp

if __name__ == '__main__':
    waitress.serve(app=yourapp, port=80, host='')
```
host - указываете свой IPv4 адресс


## app/
### smsc_api.py
[API](https://smsc.ru/) для отправки смс по номеру телефона

### SMS.py
 Файл для работы с API, геренирует код, отправляет и проверяет на совпадение
```
def codeGeneration(codesCount): -> code
def sendSMS(number): -> 0/1(Отправлено/не отправлено)
def checkSMS(number, code): -> True/False(Совпадает/не совпадает)
```

### init.py
Создает Flask App, которое потом запускается в main.py

### requests.py
Принимает HTTP запросы в формате JSON, обрабатывает и возвращает информацию

### db.py
Работает с базой данных SQLite 3.0, файл '../skyline.db'. Вносит изменения в базу данных или берет из нее информацию о билетах/пользователях.
