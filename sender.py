import requests
import atexit

while True:
    username = input("Type username: ")
    password = input("Type password: ")
    response = requests.post(
        'http://127.0.0.1:5000/login',
        json={'username': username, 'password': password}
    )
    if response.status_code == 200:
        break
    else:
        print('Error: ' + response.json()['error'])


def logout():
    requests.post(
        'http://127.0.0.1:5000/logout',
        json={'username': username, 'password': password}
    )


atexit.register(logout)


while True:
    text = input("Type message:")

    if len(text) == 0:
        continue

    response = requests.post(
        'http://127.0.0.1:5000/send',
        json={'username': username, 'password': password, 'text': text}
    )

    if response.status_code == 200:
        print('Message sent\n')
