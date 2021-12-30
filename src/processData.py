#----------------------------- Imports -----------------------------
#MongoDB access, install using 'pip install pymongo'
import pymongo

#Pretty print database data
import pprint

#Constants used across multiple files
import constants

print("\n----------------------------- Running processData.py -----------------------------")


#----------------------------- Connect to MongoDB -----------------------------
#Establish connection
client = pymongo.MongoClient(constants.CONN)

#Check Connection
try :
	client.admin.command('ping')
	#Trace 1: Connected to MongoDB
	print("Trace 1: Connection to MongoDB established")
except :
	#Trace 1.2: Not connected to MongoDB
	print("Trace 1.2: Connection to MongoDB failed")
	#Quit if connection cannot be established
	quit()


#Access database 
db = client.classDB

#Extract the database data
githubUser = db.githubUser.find()

print("Database : ")
#Pretty Print data
for user in githubUser :
	pprint.pprint(user)
	print()