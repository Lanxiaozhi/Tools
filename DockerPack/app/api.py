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
    print("Start Flask Server...")
    app.run(host="0.0.0.0")
