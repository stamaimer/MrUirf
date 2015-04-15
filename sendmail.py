import smtplib
import pymongo
import argparse

addr = "smtp.gmail.com"
port = 587

morf = "mr.uir.uif@gmail.com"

subject = "Hello, World!"

content = """
   Dear %s,

     This is a letter from MrUirf team.

     We started a project, to infuse netizens' Twitter tweets, Facebook statuses and GitHub repo. And here is our repository link: https://github.com/stamaimer/MrUirf.

     ----------------------------------------------
     And we need your help,  supplying us your Twitter , Facebook and GitHub id ( or username ).
     Your tweets, statuses and repos info will be used to:

     1. entity recognition & relation words extraction.
     2. tweets & statuses similarity calculation.
     3. generate social graph.

     * and we will never leak your info to others people or organisations.
     ----------------------------------------------
     Please reply your info in json format:

     ex. {"github":"curme", "facebook":"https://www.facebook.com/hui.zhan.796", "twitter":"curmium"}

     1.github: your "login"(the second line below your avatar) 
     2.facebook: your homepage url
     3.twitter: screen name ( ps. screen name is the name that your friends use to @ you. ex. '@curmium')
     ----------------------------------------------
     Your supports are really meaningful for us!
     Thank you gratefully!

   Sincerely,
   MrUirf.
"""

def sendmail(usr, psd, morf, tolist, subject, content):

	msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (morf, tolist[0], subject, content)

	try:

		server = smtplib.SMTP(addr, port)

		server.ehlo()

		server.starttls()

		server.ehlo()

		server.login(usr, psd)

		server.sendmail(morf, tolist, msg)

		server.close()

		print "successfully sent the mail..."

	except:

		print "failed to send mail..."

		raise

def get_user_list():

	mongo_client = pymongo.MongoClient('127.0.0.1', 27017)

	msif = mongo_client.msif

	github_users = msif.github_users

	items = github_users.find({}, {"login":1, "email":1, "_id":0})

	items = ( {"login":item["login"], "email":item["email"]} \
			  for item in items \
			  if item.has_key("email") \
			  and item["email"] != None \
			  and item["email"] != '')

	return items

if __name__ == '__main__':
	
	argument_parser = argparse.ArgumentParser(description="")

	argument_parser.add_argument("usr", help="")

	argument_parser.add_argument("psd", help="")

	args = argument_parser.parse_args()

	usr = args.usr
	psd = args.psd

	user_list = get_user_list()

	user_list = [{"login":"stamaimer", "email":"stamaimer@gmail.com"}]

	for user in user_list:

		sendmail(usr, psd, usr, [user["email"]], subject, content % user["login"])
