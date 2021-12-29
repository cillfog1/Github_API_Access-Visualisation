#import PyGithub library, install using 'pip install PyGithub' 
from github import Github

g = Github("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")

usr = g.get_user()
print("user: " + usr.login)
print("fullname: " + usr.name)
print("location: " + usr.location)
print("company: " + usr.company)