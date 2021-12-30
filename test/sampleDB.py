#----------------------------- Imports -----------------------------
#Converts dictionary to string
import json

#MongoDB access, install using 'pip install pymongo'
import pymongo

print("\n----------------------------- Running sampleDB.py -----------------------------")


#----------------------------- Initialise Data -----------------------------

dct = {	'_id' : "cillfog1",
		'user' : "cillfog1",
		'fullname' : "Cillian Fogarty",
		'location' : "Offaly, Ireland",
		'company' : "Trinity College Dublin"}

#Trace 1: Shows current data in dictionary, before being cleaned
print("Trace 1: dictionary : " + json.dumps(dct))


#----------------------------- Connect to MongoDB -----------------------------
#Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Check Connection
try :
	client.admin.command('ping')
	#Trace 3: Connected to MongoDB
	print("Trace 2: Connection to MongoDB established")
except :
	#Trace 3.2: Not connected to MongoDB
	print("Trace 2.2: Connection to MongoDB failed")
	#Quit if connection cannot be
	quit()

#Create database 
db = client.classDB

#Insert cleaned database data
try :
	db.githubUser.insert_many([dct])
	#Trace 3: Data inserted into database
	print("Trace 3: Data inserted into database")
except :
	#Trace 3.2: Username already exists in database
	print("Trace 3.2: Username already exists in database")