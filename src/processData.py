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

	with open('csv/contributerData.csv', 'w') as file :
		file.write('Date,Additions,Deletions,Total\n')
		for data in githubData :
			pprint.pprint(data)
			print()
			file.write(	str(data['date']) + ',' +
						str(data['additions']) + ',' +
						str(data['deletions']) + ',' +
						str(data['total']) + '\n')

	#Average of other members of the team
	#Extract the database data
	repoData = reposDB.find({"repoName": repoName})
	numOfContributers = 0
	for data in repoData :
		print("Contributers to repo : " + repoName)
		for user in data['contributers'] :
			pprint.pprint(user['username'])
			print()
			numOfContributers += 1

	if (numOfContributers > 1) :
		githubData = commitsDB.find({"repoName": repoName, "username": { "$ne" : username}})

		print("Database : ")
		#Pretty Print data

		with open('csv/teamData.csv', 'w') as file :
			file.write('Date,Additions,Deletions,Total\n')

			previousDate = 0
			totalAdditions = 0
			totalDeletions = 0
			totalTotal = 0
			for data in githubData :
				pprint.pprint(data)
				print()

				if (previousDate != data['date'] and previousDate != 0) :
					file.write(	str(previousDate) + ',' +
							str(totalAdditions / (numOfContributers - 1)) + ',' +
							str(totalDeletions / (numOfContributers - 1)) + ',' +
							str(totalTotal / (numOfContributers - 1)) + '\n')
					totalAdditions = 0
					totalDeletions = 0
					totalTotal = 0

				previousDate = data['date']
				totalAdditions += data['additions']
				totalDeletions += data['deletions']
				totalTotal += data['total']
			file.write(	str(previousDate) + ',' +
						str(totalAdditions / (numOfContributers - 1)) + ',' +
						str(totalDeletions / (numOfContributers - 1)) + ',' +
						str(totalTotal / (numOfContributers - 1)) + '\n')
	else :
		with open('csv/teamData.csv', 'w') as file :
			file.write('Date,Additions,Deletions,Total\n')
			file.write(	0 + '\n')