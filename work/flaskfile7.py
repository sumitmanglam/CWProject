from flask import render_template, Flask 

app= Flask(__name__)
@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    #user = {'nickname': 'Miguel'}  # fake user
    #return render_template('index.html',title='Home',user=user)
    return render_template('hello.html', name=name)

if __name__=='__main__':
	app.run('172.16.2.84','9867')	