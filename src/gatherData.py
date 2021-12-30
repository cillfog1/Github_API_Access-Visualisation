#----------------------------- Imports -----------------------------
#import PyGithub library, install using 'pip install PyGithub' 
from github import Github

#Converts dictionary to string
import json

#MongoDB access, install using 'pip install pymongo'
import pymongo

print("\n----------------------------- Running gatherData.py -----------------------------")


#----------------------------- Collect Data -----------------------------
g = Github("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")

usr = g.get_user()

dct = {	'_id' : usr.login,
		'user' : usr.login,
		'fullname' : usr.name,
		'location' : usr.location,
		'company' : usr.company}

#Trace 1: Shows current data in dictionary, before being cleaned
print("Trace 1: dictionary : " + json.dumps(dct))


#----------------------------- Clean Data -----------------------------
for k, v in dict(dct).items() :
	if v is None :
		del dct[k]

#Trace 2: Shows current data in dictionary, after being cleaned
print("Trace 2: cleaned dictionary : " + json.dumps(dct))


#----------------------------- Connect to MongoDB -----------------------------
#Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Check Connection
try :
	client.admin.command('ping')
	#Trace 3: Connected to MongoDB
	print("Trace 3: Connection to MongoDB established")
except :
	#Trace 3.2: Not connected to MongoDB
	print("Trace 3.2: Connection to MongoDB failed")
	#Quit if connection cannot be
	quit()

#Create database 
db = client.classDB

#Insert cleaned database data
try :
	db.githubUser.insert_many([dct])
	#Trace 4: Data inserted into database
	print("Trace 4: Data inserted into database")
except :
	#Trace 4.2: Username already exists in database
	print("Trace 4.2: Username already exists in database")