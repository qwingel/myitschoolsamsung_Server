import waitress
from app import yourapp

if __name__ == '__main__':
    waitress.serve(app=yourapp, port=80, host='192.168.8.52')