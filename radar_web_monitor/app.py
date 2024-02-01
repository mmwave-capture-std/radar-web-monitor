import subprocess
import shlex

from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def execute_command(command):
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    for line in iter(process.stdout.readline, ""):
        yield line
    process.stdout.close()
    process.wait()


@app.route("/execute", methods=["POST"])
def execute():
    command = request.form["command"]
    return Response(execute_command(command), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
