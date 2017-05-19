from flask import Flask
from flask import request
from flask import url_for ,redirect
from flask import render_template

import time
import sys
from flask import jsonify

app=Flask('__name__')

from cassandra.query import SimpleStatement
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

print "Cassandra connection initialized"
cluster = Cluster(
	contact_points = ['172.16.0.27','172.16.0.29'],
	load_balancing_policy=DCAwareRoundRobinPolicy(local_dc="datacenter1")
)
session = cluster.connect('cw')

CASSANDRA_KEYS_TABLE='bhrigukeystracking'

@app.route('/')

@app.route("/view")
def GetKeys():
	try:
		query = "SELECT * FROM {}".format(CASSANDRA_KEYS_TABLE)
		
		data=[]
		categories=[]
		actions=[]
		for row in session.execute(query):
			#print type(row.isactive)
			if row.isactive==True:
				data.append(row)
				categories.append(row.category)
				actions.append(row.action)
				#data=data.append([row.category,row.actions])
		
		return render_template('viewkeys.html',data=data)
		#return categories[:-1]
	except:
		print "cought"
		print sys.exc_info()
@app.route("/add")
def add():
	return render_template('add_form.html')

@app.route('/insert/',methods = ['POST'])
def AddKeys():
	#print 'hello'
	#return "hellow"
	e1 = request.form['category']
	e2 = request.form['action']
	e3 = time.strftime('%Y-%m-%dT%H:%M:%S')
	e4 = True
	#print e1, e2, e3, e4
	try:
		query="INSERT INTO {} (category,action,createddate,isactive) values ('{}','{}','{}',{})".format(CASSANDRA_KEYS_TABLE,e1,e2,e3,e4)
		session.execute(query)
		#return e1+e2+e3
		return jsonify({'cat': e1,'act': e2,'dat': e3})
	except:
		print "Caught"
		return sys.exc_info()


if __name__ == '__main__':
    app.run(debug=True)
    #app.run('172.16.2.84','9874')
