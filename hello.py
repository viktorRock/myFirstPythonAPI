from flask import Flask
app = Flask(__name__)

@app.route('/')
def response():
	return 'hello world ! :P'
