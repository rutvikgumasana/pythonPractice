from flask import Flask, request

from auth import authSignup, authLogin

app = Flask(__name__)


# @app.route('/user/<int:name>')
# def hello(name):
#     return f"hello {name}"
@app.route('/')
def hello():
    return f"hello "


@app.route('/signup', methods=['POST'])
def signup():
    return authSignup(request)


@app.route('/login', methods=['POST'])
def login():
    return authLogin(request)


if __name__ == '__main__':
    app.run()
