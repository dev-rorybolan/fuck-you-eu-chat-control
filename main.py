from flask import Flask, render_template, redirect, url_for, session, request
from flask_socketio import SocketIO, send, emit

from db import Database

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = 'fuck_you_eu_chat_control'
socketio: SocketIO = SocketIO(app)
database: Database = Database()
@app.route('/')
def index():
    return render_template('entry.html')


@socketio.on('connect', namespace='/general')
def connect_general(auth=None):
    data_general = database.load_messages(channel="general")
    for message in data_general:
        emit(
            'message',
            f"{message['username']} | {message['text']}",
            namespace='/general',
            to=request.sid
        )

@socketio.on('connect', namespace="/gaming")
def connect_gaming(auth=None):
    data_gaming = database.load_messages(channel="gaming")
    for message in data_gaming:
        emit(
            'message',
            f"{message['username']} | {message['text']}",
            namespace='/gaming',
            to=request.sid
        )
@app.route("/login", methods=["POST"])
def login():
    username: str = request.form["username"]
    session["username"] = username
    return redirect(url_for("general"))

@app.route("/general")
def general():
    return render_template("index.html")

@app.route("/gaming")
def gaming():
    return render_template("gaming.html")

@socketio.on('message', namespace='/general')
def handle_general_message(data):
    username = data.get("username", "Anonymous")
    msg = data.get("msg", "")
    database.post_message(username=username, msg=msg, channel="general")
    print(f"[GENERAL] {username}: {msg}")
    send(f"{username} | {msg}", broadcast=True, namespace='/general')



@socketio.on('message', namespace='/gaming')
def handle_gaming_message(data):
    username = data.get("username", "Anonymous")
    msg = data.get("msg", "")
    database.post_message(username=username, msg=msg, channel="gaming")
    print(f"[GAMING] {username}: {msg}")
    send(f"{username} | {msg}", broadcast=True, namespace='/gaming')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
