from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome!'


@app.route('/api/show', methods=['POST', 'GET'])
def show():
    if request.method == 'POST':
        return "POST METHOD!"
    if request.method == 'GET':
        return "GET METHOD!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
