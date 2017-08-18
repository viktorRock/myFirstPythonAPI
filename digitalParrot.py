from flask import flask

app = Flask(__name__)

@app.route('/')
def response():
	return 'hello world ! :P'
