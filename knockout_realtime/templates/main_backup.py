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
  return render_template('viewkeys.html')
@app.route("/view")
def GetKeys():
  try:
    query = "SELECT * FROM {}".format(CASSANDRA_KEYS_TABLE)
    data=[]
    
    for row in session.execute(query):
      print type(row)
      if row.isactive:
        #data.append(row)
        data.append({'category': row.category,'action': row.action,'createddate': row.createddate.strftime('%Y-%m-%dT%H:%M:%S'),'wantdelete':False})
        
    return jsonify(data)
    #return categories[:-1]
  except:
    return "cought"
    return sys.exc_info()
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
    query="SELECT * FROM {} WHERE category = '{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,e1,e2)
    for row in session.execute(query):
      return "",304

    query="INSERT INTO {} (category,action,createddate,isactive) values ('{}','{}','{}',{})".format(CASSANDRA_KEYS_TABLE,e1,e2,e3,e4)
    session.execute(query)
    return jsonify({'cat': e1,'act': e2,'dat': e3})
  except:
    print "Caught"
    return sys.exc_info()

@app.route('/insert_into_main/',methods = ['POST'])
def AddRealTimeKeys():
  #print 'hello'
  #return "hellow"
  e1 = request.form['category']
  e2 = request.form['action']

  #print e1, e2, e3, e4
  try:
  	query="UPDATE {} SET isrealtimeactive=True WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,e1,e2)       
    session.execute(query)
    return "real time active"

    
  except:
    print "Caught real time"
    return sys.exc_info()

@app.route('/delete/',methods = ['POST'])
def delete():

  e1 = request.form['category']
  e2 = request.form['action']
  key=e1+e2
  try:
    #deleting from key table
    query="UPDATE {} SET isactive=False WHERE category='{}' AND action='{}'".format(CASSANDRA_KEYS_TABLE,e1,e2)       
    session.execute(query)
    print "deleted from key table"

    #deleting from real time key table
    query="UPDATE {} SET isactive=False WHERE key='{}'".format(CASSANDRA_REAL_TIME_KEYS_TABLE,key)        
    session.execute(query)
    print "deleted from real time key table"
    return "done"
  except:
    return sys.exc_info()


if __name__ == '__main__':
    app.run(debug=True)
    #app.run('172.16.2.84','5000')
