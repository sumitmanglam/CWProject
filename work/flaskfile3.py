from flask import Flask

app= Flask(__name__)

@app.route('/<username>')

def show_user_profile(username):
	return 'user %s' % username

if __name__=='__main__':
	app.run('172.16.2.84','9872')