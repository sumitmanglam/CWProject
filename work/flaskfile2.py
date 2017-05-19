from flask import Flask

app=Flask(__name__)

@app.route("/hello")
def hello_world():
	x = index()
	return "hello world "+ x

@app.route("/")
def index():
	return "index"




if __name__=='__main__':
	app.run('172.16.2.84','9873')
