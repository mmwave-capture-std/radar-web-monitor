import base64
import io
import os
import subprocess
import shlex
import json
import pathlib

import pickle
import copy

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "oaiesnt#!ehA21$&ndhienasrUns"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


def send_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        socketio.emit("image", encoded_string)


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


@socketio.on("get_plot")
def handle_get_plot(json):
    plot_num = int(json["plot_num"])
    pickles = sorted(pathlib.Path("latest").glob("*.pickle"))
    data = pickle.load(open(pickles[plot_num], "rb"))
    socketio.emit("data", {"data": data, "pk": plot_num})


@socketio.on("inference_latest")
def handle_inference_latest(json):
    pickles = sorted(pathlib.Path("latest_fft").glob("*.pickle"))

    from ConcealedWeaponDetection import test_single

    (
        classification,
        left_chest,
        right_chest,
        left_pocket,
        right_pocket,
    ) = test_single.test(pickles[0], "ConcealedWeaponDetection/test_rd104")

    right_chest = right_chest.astype(float).tolist()
    left_chest = left_chest.astype(float).tolist()
    right_pocket = right_pocket.astype(float).tolist()
    left_pocket = left_pocket.astype(float).tolist()
    classification = classification.astype(float)
    classes = ["without", "left chest", "right chest", "left pocket", "right pocklet"]
    most_possible = np.argmax(classification)
    part_probabilities = np.array(
        [left_chest, right_chest, left_pocket, right_pocket], dtype=float).tolist()

    heat_data = [
        {"x": 90, "y": 120, "value": right_chest[-1]},
        {"x": 120, "y": 120, "value": left_chest[-1]},
        {"x": 90, "y": 180, "value": right_pocket[-1]},
        {"x": 120, "y": 180, "value": left_pocket[-1]},
    ]

    socketio.emit(
        "inference",
        {
            "classification": classification.tolist(),
            "classes": classes,
            "most_possible_class": classes[most_possible],
            "most_possible_class_probability": classification[most_possible],
            "part_probabilities": part_probabilities,
            "heat_data": heat_data,
        },
    )


@socketio.on("execute_command")
def handle_execute_command(json):
    command = json["command"]
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "x"
    socketio.start_background_task(background_thread, command, env=env)


if __name__ == "__main__":
    socketio.run(app, debug=True)
    # app.run(debug=True)
