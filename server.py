import time
from flask import Flask, request
from datetime import datetime
import hashlib

app = Flask(__name__)

messages = [
    {'username': 'Bot', 'time': time.time(), 'text': 'Chat created'}
]
users = dict()
users_online = set()


def create_password(password):
    return hashlib.sha1(password.encode()).hexdigest()


def check_password(password, hash_password):
    return hashlib.sha1(password.encode()).hexdigest() == hash_password


@app.route("/")
def hello_method():
    return "Hello, World! 123"


@app.route("/status")
def status_method():
    return {
        'status': True,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'users': len(users),
        'users_online': len(users_online),
        'messages': len(messages)
    }


@app.route("/login", methods=['POST'])
def login_method():
    """
    JSON {"username": str, "password": str}
    :return: {'ok': bool}
    """
    username = request.json['username']
    password = request.json['password']

    if not isinstance(username, str) or len(username) == 0:
        return {'error': 'Empty username'}, 401

    if username not in users:
        users[username] = create_password(password)
    elif not check_password(password, users[username]):
        return {'error': 'Invalid password'}, 401
    users_online.add(username)
    messages.append({
        'username': 'Bot',
        'time': time.time(),
        'text': username + ' joined the chat'
    })
    return {'ok': True}


@app.route("/logout", methods=['POST'])
def logout_method():
    """
    JSON {"username": str, "password": str}
    :return: {'ok': bool}
    """
    username = request.json['username']
    password = request.json['password']
    if username in users_online and check_password(password, users[username]):
        users_online.remove(username)
        messages.append({
            'username': 'Bot',
            'time': time.time(),
            'text': username + ' left the chat'
        })
        return {'ok': True}
    return {'ok': False}


@app.route("/send", methods=['POST'])
def send_method():
    """
    JSON {"username": str, "password": str, "text": str}
    username, text - непустые строки
    :return: {'ok': bool}
    """
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    # first attempt for password is always valid
    if username not in users:
        users[username] = create_password(password)

    # validate data
    if not isinstance(text, str) or len(text) == 0:
        return {'ok': False}, 403
    if username not in users or not check_password(password, users[username]):
        return {'ok': False}, 401

    # TODO save message
    messages.append({'username': username, 'time': time.time(), 'text': text})

    if text == '/status':
        messages.append({
            'username': 'Bot',
            'time': time.time(),
            'text': '\n'.join([f'"{k}": {v}' for k, v in status_method().items()])
        })

    return {'ok': True}


@app.route("/messages")
def messages_method():
    """
    Param after - отметка времени после которой будут сообщения в результате
    username, text - непустые строки
    :return: {'messages': [
        {'username': str, 'time': float, 'text': str},
        ...
    ]}
    """
    after = float(request.args['after'])
    filtered_messages = [message for message in messages if message['time'] > after]

    return {'messages': filtered_messages}


def run_server():
    app.run(debug=True)
