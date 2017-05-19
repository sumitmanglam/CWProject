from flask import Flask 
app= Flask('__name__')

@app.route('/<nickname>')
def index(nickname):
	user={nickname:'sumit'}
	return '''
	<html>
		<head>
			<title> Home Page </title>
		</head>

		<body>
		<h1> Hello, ''' + user[nickname] + ''' </h1>
		</body>
	</html>
	'''

if __name__=='__main__':
	app.run('172.16.2.84','9868')