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

#Repo database
reposDB = db.repos

#Commit database
commitsDB = db.commits

def extractData(repoName, username) :
	#Extract the database data
	githubData = commitsDB.find({"repoName": repoName, "username": username})

	print("Database : ")
	#Pretty Print data

	with open('csv/data.csv', 'w') as file :
		file.write('Date,Additions,Deletions,Total\n')
		for data in githubData :
			pprint.pprint(data)
			print()
			file.write(	str(data['date']) + ',' +
						str(data['additions']) + ',' +
						str(data['deletions']) + ',' +
						str(data['total']) + '\n')