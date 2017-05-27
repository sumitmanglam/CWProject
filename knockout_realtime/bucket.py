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

CASSANDRA_REAL_TIME_KEYS_TABLE='realtimeeventtrackingkeys'

@app.route("/")
def load():
	try:
		query = "SELECT * FROM {}".format(CASSANDRA_REAL_TIME_KEYS_TABLE)
		data=[]
		for row in session.execute(query):
			if row.isactive:
				data.append(row)#{'key': row.key,'createddate': row.createddate.strftime('%Y-%m-%dT%H:%M:%S')})
		return render_template('bucket_index.html',data=data)
	except:
		print sys.exc_info()


if __name__ == '__main__':
    app.run(debug=True)
    #app.run('172.16.2.84','5000')




 