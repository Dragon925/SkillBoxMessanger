import requests
import datetime
import time

last_received = 0

while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': last_received}
    )

    if response.status_code == 200:
        messages = response.json()['messages']
        for message in messages:
            print(message['username'],
                  datetime.datetime.fromtimestamp(message['time']).strftime('%Y-%m-%d %H:%M:%S'))
            print(message['text'])
            print()
            last_received = message['time']
    time.sleep(1)