from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # for session encryption
socketio = SocketIO(app)  # initialize SocketIO

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(msg):
    print(f'Received message: {msg}')
    send(f'Rory | {msg}', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
