from flask import Flask 
from flask import request,url_for,redirect

app=Flask(__name__)

@app.route('/success/<name>')
def success(name):
	return 'welcome %s ' % name
@app.route('/login',methods=['GET','POST'])

def login():
	if request.method=='POST':
		user= request.form['nm']
		return redirect(url_for('success',name=user))
	else:
		user=request.args.get('nm')
		return redirect(url_for('success',name=user))


if __name__=='__main__':
	app.run('172.16.2.84','9869')