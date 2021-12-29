#import PyGithub library, install using 'pip install PyGithub' 
from github import Github

g = Github("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")

usr = g.get_user()
print("user: " + usr.login)

if usr.name is not None:
	print("fullname: " + usr.name)

if usr.location is not None:
	print("location: " + usr.location)

if usr.company is not None:
 print("company: " + usr.company)