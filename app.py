import os
import socket
from flask import Flask, render_template

app = Flask(__name__)

# Read App Version from env (Default v1)
APP_VERSION = os.getenv("APP_VERSION", "v1")

@app.route("/")
def index():
    # Current pod hostname - To identify the request from which pod comming
    pod_name = socket.gethostname()
    return render_template("index.html", version=APP_VERSION, pod=pod_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)