#----------------------------- Imports -----------------------------
#import PyGithub library, install using 'pip install PyGithub' 
from github import Github

#Pretty print dictionary data
import pprint

#MongoDB access, install using 'pip install pymongo'
import pymongo

#Constants used across multiple files
import constants

#Date formatting
from datetime import datetime

#To anonymise names
from faker import Faker
from collections import defaultdict
faker = Faker()
names = defaultdict(faker.name)

print("\n----------------------------- Running gatherData.py -----------------------------")


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
	#Quit if connection cannot be
	quit()


#----------------------------- MongoDB Databases -----------------------------
#Create database 
db = client.classDB

#Repo database
reposDB = db.repos

#Set unique identifier as repoName
reposDB.create_index([("repoName", pymongo.ASCENDING)], unique=True)

#Commit database
commitsDB = db.commits


#----------------------------- Collect Data -----------------------------
def collectData(repoName) :
	if (constants.GITHUB_TOKEN == 0) :
		print("\nIMPORTANT: Please insert your API token in src/constants.py")
		quit()
	g = Github(constants.GITHUB_TOKEN)


	#----------------------------- Repos -----------------------------
	#Get repo
	repo = g.get_repo(repoName)

	#If repo does not already exist in database
	if (reposDB.count_documents({"repoName": repoName}) < 1) :
		#Get contributers
		contributers = [] #default value
		contributersList = g.get_repo(repoName).get_contributors()
		for contributer in contributersList :
			#Anonymise names?
			if (constants.ANONYMISE_NAMES == 1) :
				username = names[contributer.login].replace(" ", ""), #Anonymising username
				fullName = names[contributer.name]
			else :
				username = contributer.login
				fullName = contributer.name

			contributerDct = {	'username' : username,
								'fullName' : fullName}
			contributers.append(contributerDct)

		repoDct = {	'repoName' : repoName,
					'contributers' : contributers}

		#Trace 2: Shows current data in repo dictionary
		print("Trace 2: repo dictionary : ")
		pprint.pprint(repoDct)
		print()

		#----------------------------- Insert into Repo database -----------------------------
		reposDB.insert_many([repoDct])
		#Trace 3: Data inserted into database
		print("Trace 3: Data inserted into database\n")


		#----------------------------- Merge all commits by date -----------------------------
		#This means the graph is less clutters with multiple commits made on the same day,
		#instead collating/merging all bulk modifications made by a single person, on a particular day into one point

		#Reversed to start at oldest commit and work to most recent commit
		commits = repo.get_commits().reversed

		#Default Values
		previousCommitDct = {	'repoName' : "",
								'username' : "",
								'date' : "",
								'additions' : 0,
								'deletions' : 0,
								'total' : 0}
		commitsByDate = []

		for commit in commits :
			#Anonymise names?
			if (constants.ANONYMISE_NAMES == 1) :
				username = names[commit.author.login].replace(" ", ""), #Anonymising username
			else :
				username = commit.author.login

			#Date of commit
			date = commit.commit.author.date.strftime("%Y/%m/%d")

			#If previous commit was made on the same day, by the same person merge them
			if (username == previousCommitDct['username'] and date == previousCommitDct['date']) :
				commitDct = {	'repoName' : repoName,
								'username' : username,
								'date' : date,
								'additions' : previousCommitDct['additions'] + commit.stats.additions,
								'deletions' : previousCommitDct['deletions'] + commit.stats.deletions,
								'total' : previousCommitDct['total'] + commit.stats.total}

			else :
				#If not first run
				if (previousCommitDct['date'] != "") :
					commitsByDate.append(previousCommitDct)
					#Trace 4: Shows current data in dictionary, before being cleaned
					print("Trace 4: added to commitsByDate list : ")
					pprint.pprint(previousCommitDct)
					print()

				commitDct = {	'repoName' : repoName,
								'username' : username,
								'date' : date,
								'additions' : commit.stats.additions,
								'deletions' : commit.stats.deletions,
								'total' : commit.stats.total}
			#Update previous
			previousCommitDct = commitDct

		#Add last
		commitsByDate.append(previousCommitDct)

		#For all commits after merging
		for commitDct in commitsByDate :
			#----------------------------- Clean Data -----------------------------
			for k, v in dict(commitDct).items() :
				if v is None :
					del commitDct[k]

			#Trace 5: Shows current data in dictionary, after being cleaned
			print("Trace 5: cleaned commit dictionary : ")
			pprint.pprint(commitDct)
			print()


			#----------------------------- Insert into database -----------------------------
			commitsDB.insert_many([commitDct])
			#Trace 6: Data inserted into database
			print("Trace 6: Data inserted into database\n")
		return repoDct

	else :
		#Trace 7: Repo already exists in database
		print("Trace 7: " + repoName + " already exists in database\n")

		repoData = reposDB.find({"repoName": repoName})
		contributers = [] #default value
		for data in repoData :
			print("Contributers to repo : " + repoName)
			for user in data['contributers'] :
				contributerDct = {	'username' : user['username'],
									'fullName' : user['fullName']}
				contributers.append(contributerDct)
				pprint.pprint(contributerDct)
				print()
				
		repoDct = {	'repoName' : repoName,
			'contributers' : contributers}
		return repoDct