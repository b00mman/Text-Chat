import websockets
import asyncio
import json
import sqlite3

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit

async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

@app.route("/")
def main():
    return render_template("index.html", sync_mode=socketio.async_mode)

db = sqlite3.connect("messages.db")
print(db.execute("SELECT * FROM Messages").fetchall())

@socketio.event
def fetch():
    log = db.execute("SELECT * FROM Messages").fetchall()
    for i in log:
        event = {"text": i[0], "user": i[1]}
        emit("message", json.dumps(event))

@socketio.event
def message(json):
    event = {"text": message["text"], "user": message["user"]}
    emit("message", json.dumps(event), broadcast=True)
    db.execute("INSERT INTO Messages (Message, User) VALUES ('{}', '{}');".format(message["text"].replace("'","''"), message["user"].replace("'","''")))
    db.commit()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")