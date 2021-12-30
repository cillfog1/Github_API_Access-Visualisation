#----------------------------- Imports -----------------------------
#import PyGithub library, install using 'pip install PyGithub' 
from github import Github

#Converts dictionary to string
import json

#MongoDB access, install using 'pip install pymongo'
import pymongo

#Constants used across multiple files
import constants

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


#----------------------------- Collect Data -----------------------------
if (constants.GITHUB_TOKEN == 0) :
	print("\nIMPORTANT: Please insert your API token in src/constants.py")
	quit()
g = Github(constants.GITHUB_TOKEN)

repo = g.get_repo("EndaHealion/AlgoDats-Bus-Management")
commits = repo.get_commits()

commitNumber = 1

for commit in commits :
	#Anonymise names?
	if (constants.ANONYMISE_NAMES == 1) :
		username = names[commit.author.login].replace(" ", ""), #Anonymising username
		fullName = names[commit.author.name], #Anonymising name
	else :
		username = commit.author.login
		fullName = commit.author.name

	dct = {	'commitNumber' : commitNumber,
			'user' : username,
			'fullName' : fullName,
			'additions' : commit.stats.additions,
			'deletions' : commit.stats.deletions}
	commitNumber += 1

	#Trace 2: Shows current data in dictionary, before being cleaned
	print("Trace 2: dictionary : " + json.dumps(dct))


	#----------------------------- Clean Data -----------------------------
	for k, v in dict(dct).items() :
		if v is None :
			del dct[k]

	#Trace 3: Shows current data in dictionary, after being cleaned
	print("Trace 3: cleaned dictionary : " + json.dumps(dct))


	#----------------------------- Insert into database -----------------------------
	db.githubUser.insert_many([dct])
	#Trace 4: Data inserted into database
	print("Trace 4: Data inserted into database\n")