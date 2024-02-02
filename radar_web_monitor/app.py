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


def background_thread(command):
    """Run a command and emit stdout lines to a WebSocket."""
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in iter(process.stdout.readline, ""):
        socketio.emit("command_output", {"data": line})
    process.stdout.close()
    process.wait()


@socketio.on("execute_command")
def handle_execute_command(json):
    command = json["command"]
    socketio.start_background_task(background_thread, command)


if __name__ == "__main__":
    app.run(debug=True)
