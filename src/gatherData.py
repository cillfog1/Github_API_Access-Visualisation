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

#Create database 
db = client.classDB

#Repo database
reposDB = db.repos

#Commit database
commitsDB = db.commits

#----------------------------- Collect Data -----------------------------
def collectData(repoName) :
	if (constants.GITHUB_TOKEN == 0) :
		print("\nIMPORTANT: Please insert your API token in src/constants.py")
		quit()
	g = Github(constants.GITHUB_TOKEN)

	repo = g.get_repo(repoName)
	#Reversed to start at oldest commit and work to most recent commit
	commits = repo.get_commits().reversed

	for commit in commits :
		#Anonymise names?
		if (constants.ANONYMISE_NAMES == 1) :
			username = names[commit.author.login].replace(" ", ""), #Anonymising username
		else :
			username = commit.author.login

		date = commit.commit.author.date.strftime("%Y/%m/%d")

		dct = {	'repoName' : repoName,
				'username' : username,
				'date' : commit.commit.author.date.strftime("%Y/%m/%d"),
				'additions' : commit.stats.additions,
				'deletions' : commit.stats.deletions,
				'total' : commit.stats.total}

		#Trace 2: Shows current data in dictionary, before being cleaned
		print("Trace 2: dictionary : ")
		pprint.pprint(dct)
		print()


		#----------------------------- Clean Data -----------------------------
		for k, v in dict(dct).items() :
			if v is None :
				del dct[k]

		#Trace 3: Shows current data in dictionary, after being cleaned
		print("Trace 3: cleaned dictionary : ")
		pprint.pprint(dct)
		print()


		#----------------------------- Insert into database -----------------------------
		commitsDB.insert_many([dct])
		#Trace 4: Data inserted into database
		print("Trace 4: Data inserted into database\n")