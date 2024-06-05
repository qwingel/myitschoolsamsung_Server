import requests


response = requests.post(
    url="http://antarktida.pythonanywhere.com/login",

    json={
        "phone" : "79965909963"
    }

)
print(response.text)