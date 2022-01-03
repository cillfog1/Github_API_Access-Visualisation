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

	totalContributerAdditions = 0
	totalContributerDeletions = 0
	totalContributerTotal = 0
	with open('csv/contributerData.csv', 'w') as file :
		file.write('Date,Additions,Deletions,Total\n')
		for data in githubData :
			pprint.pprint(data)
			print()
			file.write(	str(data['date']) + ',' +
						str(data['additions']) + ',' +
						str(data['deletions']) + ',' +
						str(data['total']) + '\n')
			totalContributerAdditions += data['additions']
			totalContributerDeletions += data['deletions']
			totalContributerTotal += data['total']

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

	totalTeamAdditions = totalContributerAdditions
	totalTeamDeletions = totalContributerDeletions
	totalTeamTotal = totalContributerTotal
	if (numOfContributers > 1) :
		githubData = commitsDB.find({"repoName": repoName, "username": { "$ne" : username}})

		print("Database : ")
		#Pretty Print data

		with open('csv/teamAverageData.csv', 'w') as file :
			file.write('Date,Additions,Deletions,Total\n')

			previousDate = 0
			totalAdditions = 0
			totalDeletions = 0
			totalTotal = 0
			contributersToday = []
			numOfContributersToday = 0
			for data in githubData :
				pprint.pprint(data)
				print()

				if (previousDate != data['date'] and previousDate != 0) :
					file.write(	str(previousDate) + ',' +
							str(totalAdditions / numOfContributersToday) + ',' +
							str(totalDeletions / numOfContributersToday) + ',' +
							str(totalTotal / numOfContributersToday) + '\n')

					totalTeamAdditions += totalAdditions
					totalTeamDeletions += totalDeletions
					totalTeamTotal += totalTotal

					totalAdditions = 0
					totalDeletions = 0
					totalTotal = 0
					contributersToday = []
					numOfContributersToday = 0

				if (data['username'] not in contributersToday) :
					contributersToday.append(data['username'])
					numOfContributersToday += 1

				previousDate = data['date']
				totalAdditions += data['additions']
				totalDeletions += data['deletions']
				totalTotal += data['total']

			file.write(	str(previousDate) + ',' +
						str(totalAdditions / numOfContributersToday) + ',' +
						str(totalDeletions / numOfContributersToday) + ',' +
						str(totalTotal / numOfContributersToday) + '\n')

			totalTeamAdditions += totalAdditions
			totalTeamDeletions += totalDeletions
			totalTeamTotal += totalTotal

	else :
		with open('csv/teamAverageData.csv', 'w') as file :
			file.write('Date,Additions,Deletions,Total\n')
			#Empty file
			file.write(	"0000/00/00,0,0,0\n")

	statsDct = {	'totalContributerAdditions' : totalContributerAdditions,
					'totalContributerDeletions' : totalContributerDeletions,
					'totalContributerTotal' : totalContributerTotal,
					'totalAverageTeamMemberAdditions' : round((totalTeamAdditions / numOfContributers), 2),
					'totalAverageTeamMemberDeletions' : round((totalTeamDeletions / numOfContributers), 2),
					'totalAverageTeamMemberTotal' : round((totalTeamTotal / numOfContributers), 2),
					'totalTeamAdditions' : totalTeamAdditions,
					'totalTeamDeletions' : totalTeamDeletions,
					'totalTeamTotal' : totalTeamTotal}

	return statsDct