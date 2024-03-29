#----------------------------- Imports -----------------------------
#MongoDB access, install using 'pip install pymongo'
import pymongo

print("\n----------------------------- Running clearDB.py -----------------------------")


#----------------------------- Connect to MongoDB -----------------------------
#Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

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

#Repo database
reposDB = db.repos

#Commit database
commitsDB = db.commits

#Clear repos database
reposDB.delete_many({})

#Trace 2: githubUser database cleared
print("Trace 2: reposDB database cleared")

#Clear commits database 
commitsDB.delete_many({})

#Trace 2: githubUser database cleared
print("Trace 3: commitsDB database cleared")