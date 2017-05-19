from flask import Flask,session 
import os

app= Flask('__name__')

app.secret_key=os.urandom(24)

@app.route('/')
def index():
	session['user']='anthony'
	return 'Index'
app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']

	else:
		return 'not logged in! '
def dropsession():
	session.pop('user',None)
	return 'Dropped! '
if __name__=='__main__':
	app.run('172.16.2.84','9865')