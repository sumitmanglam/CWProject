from flask import Flask
from flask import request
from flask import url_for ,redirect
from flask import render_template
import sys

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
def index():
	return render_template('option.html')
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
		print sys.exc_info()
@app.route("/add")
def add():
	return render_template('add_form.html')

@app.route('/insert/',methods = ['POST'])
def AddKeys():
	#print 'hello'
	e1 = request.form['category']
	e2 = request.form['action']
	e3 = request.form['createddate']
	e4 = request.form['isactive']
	print e1, e2, e3, e4
	try:
		query="INSERT INTO {} (category,action,createddate,isactive) values ('{}','{}','{}',{})".format(CASSANDRA_KEYS_TABLE,e1,e2,e3,e4)
		session.execute(query)
		return redirect(url_for('GetKeys'))
	except:
		return sys.exc_info()

@app.route('/delete')
def delet():
	return render_template('delete_form.html')

@app.route('/remove/',methods=['POST'])
def RemoveKey():
	e1=request.form['category']
	e2=request.form['action']
	col="isactive"
	try:
		query="UPDATE {} SET isactive=False WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,e1,e2)
		session.execute(query)
		return redirect(url_for('GetKeys'))
	except:
		return sys.exc_info()

@app.route('/remove2/',methods=['POST'])
def RemoveKey2():
	frm=request.form
	col="isactive"
	try:
		for i in frm :
			if i!='submit':
				y=i.split('-')
				e1=y[0]
				e2=y[1]
				query="UPDATE {} SET isactive=False WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,e1,e2)
				session.execute(query)
		return redirect(url_for('GetKeys'))
	except:
		return sys.exc_info()
if __name__ == '__main__':
    app.run('172.16.2.84','9874')

