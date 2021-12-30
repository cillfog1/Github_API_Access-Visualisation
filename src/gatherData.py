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


#----------------------------- Collect Data -----------------------------
if (constants.GITHUB_TOKEN == 0) :
	print("\nIMPORTANT: Please insert your API token in constants.py")
	quit()
g = Github(constants.GITHUB_TOKEN)

usr = g.get_user()

dct = {	'_id' : names[usr.login].replace(" ", ""), #Anonymising username used as uniqueID
		'user' : names[usr.login].replace(" ", ""), #Anonymising username
		'fullname' : names[usr.name], #Anonymising name
		'location' : usr.location,
		'company' : usr.company,
		'public_repos' : usr.public_repos}

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
client = pymongo.MongoClient(constants.CONN)

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