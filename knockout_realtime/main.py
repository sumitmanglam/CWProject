from flask import Flask,jsonify
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
CASSANDRA_REAL_TIME_KEYS_TABLE='realtimeeventtrackingkeys'

@app.route('/')
def load():
  return render_template('viewkeysimages.html')

@app.route("/view")
def GetKeys():
  try:
    query = "SELECT * FROM {}".format(CASSANDRA_KEYS_TABLE)
    
    data=[]
    
    for row in session.execute(query):
        if row.isactive:
        	data.append({'category': row.category,'action': row.action,'createddate': row.createddate.strftime('%Y-%m-%dT%H:%M:%S'),'isrealtimetrackingactive': str(row.isrealtimetrackingactive)})
        
    return jsonify(data)
    #return categories[:-1]
  except:
    return "cought"
    return sys.exc_info()


@app.route('/insert/',methods = ['POST'])
def AddKeys():
  #print 'hello'
  #return "hellow"
  category = request.form['category']
  action = request.form['action']
  createddate = time.strftime('%Y-%m-%dT%H:%M:%S')
  isactive = True
  realtimeflag = False
  #print e1, e2, e3, e4
  try:
  	status = 201
  	query="SELECT * FROM {} WHERE category = '{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,category,action)
  	for row in session.execute(query):
  		if row.isactive:
  			return "Key already exists",409
  		else:
  			status = 205
  	query="INSERT INTO {} (category,action,createddate,isactive,isrealtimetrackingactive) values ('{}','{}','{}',{},{})".format(CASSANDRA_KEYS_TABLE,category,action,createddate,isactive,realtimeflag)
  	session.execute(query)
  	print "added"
  	return jsonify({'cat': category,'act': action,'dat': createddate,'realtime':str(realtimeflag)}),status
  except:
    print "Caught"
    return sys.exc_info()

@app.route('/real_time_table_operation/',methods = ['POST'])
def AddRealTimeKeys():
  #print 'hello'
  #return "hellow"
  category = request.form['category']
  action = request.form['action']
  realtimeflag = request.form['isrealtimetrackingactive']
  createddate = time.strftime('%Y-%m-%dT%H:%M:%S')
  

  key=category+'-'+action 
  #print e1, e2, e3, e4
  try:

  	print "checkpoint 0"
  	
  	query="SELECT * FROM {} WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,category,action)
  	for row in session.execute(query):
  		if not row.isactive:
  			return "This key does not exist now ",409
  	print "checkpoint 1"
  	print realtimeflag
  	if realtimeflag=="false" or realtimeflag=="False":

  		print "checkpoint 2"

  		query="SELECT * FROM {} WHERE key='{}'".format(CASSANDRA_REAL_TIME_KEYS_TABLE,key)
  		for row in session.execute(query):
  			if row.isactive:
  				return "key is already being tracked in real time",409
  		print "checkpoint 3"

  		query="INSERT INTO {} (key,createddate,isactive) values ('{}','{}',{})".format(CASSANDRA_REAL_TIME_KEYS_TABLE,key,createddate,True)
  		session.execute(query)
  		print "checkpoint 4"

  		query="UPDATE {} SET isrealtimetrackingactive=True WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,category,action)
  		session.execute(query)
  		print "checkpoint 5"
  		return "True"
  	else:
  		query="SELECT * FROM {} WHERE key='{}'".format(CASSANDRA_REAL_TIME_KEYS_TABLE,key)
    	for row in session.execute(query):
    		if not row.isactive:
      			return "key is not being tracked in real time",409


      	query="INSERT INTO {} (key,createddate,isactive) values ('{}','{}',{})".format(CASSANDRA_REAL_TIME_KEYS_TABLE,key,createddate,False)
      	session.execute(query)

      	query="UPDATE {} SET isrealtimetrackingactive=False WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,category,action)
      	session.execute(query)
      	return "False"

    
  except:
    print "Caught real time"
    return sys.exc_info()

@app.route('/delete/',methods = ['POST'])
def delete():

  category = request.form['category']
  action= request.form['action']
  key=category+'-'+action

  try:
    #deleting from key table

    query="SELECT * FROM {} WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,category,action)
    for row in session.execute(query):
  		if not row.isactive:
  			return "This key has been deleted already",409

    query="UPDATE {} SET isactive=False,isrealtimetrackingactive=False WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,category,action)       
    session.execute(query)
    query="UPDATE {} SET isactive=False WHERE key='{}'".format(CASSANDRA_REAL_TIME_KEYS_TABLE,key)       
    session.execute(query)
    
    print "deleted from key table"
    return "deleted"

  except:
    return sys.exc_info()


if __name__ == '__main__':
    app.run(debug=True)
    #app.run('172.16.2.84','5000')
