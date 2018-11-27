import argparse
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/add')
def add():
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    return str(a + b)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()

    parse.add_argument("-h", "--host", default='0.0.0.0')
    parse.add_argument("-p", "--port", type=int, default=80)

    args = parse.parse_args()
    print("Start Flask Server...")
    app.run(host="0.0.0.0")
