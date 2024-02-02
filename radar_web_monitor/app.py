import os
import subprocess
import shlex

from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "oaiesnt#!ehA21$&ndhienasrUns"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


def background_thread(command, env):
    """Run a command and emit stdout lines to a WebSocket."""
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )
    while True:
        line = process.stdout.readline()
        if not line:
            break
        socketio.emit("command_output", {"data": line})
    process.stdout.close()
    process.wait()


@socketio.on("execute_command")
def handle_execute_command(json):
    command = json["command"]
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "x"
    socketio.start_background_task(background_thread, command, env=env)


if __name__ == "__main__":
    socketio.run(app, debug=True)
    # app.run(debug=True)
