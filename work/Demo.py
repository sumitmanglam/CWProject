from flask import Flask

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

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'
@app.route("/trackingkeys")
@app.route("/trackingkeys/<category>")
def GetKeys():
	try:
		query = "SELECT * FROM {}".format(CASSANDRA_KEYS_TABLE)
		categories=''
		for row in session.execute(query):
			categories = categories + row.category + ','
		return categories[:-1]
	except:
		print sys.exc_info()
@app.route("/trakingkeys/add")
def AddKeys():
	try:
		query="INSERT INTO demo"
		
if __name__ == '__main__':
    app.run('172.16.2.84','9874')
