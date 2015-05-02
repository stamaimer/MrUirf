# -*- coding: utf-8 -*-

import time
import smtplib
import pymongo
import argparse

from email.mime.text import MIMEText

addr = "localhost" # "smtp.gmail.com"
port = 25 # 587

morf = "seboraim@gmail.com"

subject = "A Request for Twitter Screen Name and Facebook Homepage URL"

content = """
   Dear %s,

     <p>This is a letter from MrUirf team.</p>

     <p>We started a project, to infuse netizens' Twitter tweets, Facebook statuses and GitHub repo. And here is our repository link: https://github.com/stamaimer/MrUirf.</p>

     <p><b>And we need your help,  supplying us your Twitter , Facebook and GitHub id ( or username ).</b></p>

     <p>Your tweets, statuses and repos info will be used to:</p>

	 <ol>
     <li>entity recognition & relation words extraction.</li>
     <li>tweets & statuses similarity calculation.</li>
     <li>generate social graph.</li>
	 </ol>

     <p><b>* and we will never leak your info to other people or organisations.</b></p>
     
     <p><b>Please reply your info in json format:</b></p>

     <p>ex. {"github":"curme", "facebook":"https://www.facebook.com/hui.zhan.796", "twitter":"curmium"}</p>
	
	 <ol>
     <li>github: your "login"(the second line below your avatar)</li> 
     <li>facebook: your homepage url</li>
     <li>twitter: screen name ( ps. screen name is the name that your friends use to @ you. ex. '@curmium')</li>
     </ol>

     <p>If you have no Twitter or Facebook accounts, please ignore this letter.</p>

     <p>Thank you for reading this letter. Your support are really meaningful to us!</p>
     <p>Thank you gratefully!</p>

   Sincerely,
   MrUirf.
"""

# def sendmail(usr, psd, morf, tolist):
def sendmail(tolist):

	log = open("log", 'w')

	try:

		server = smtplib.SMTP(addr, port)

		# server.ehlo()

		# server.starttls()

		# server.ehlo()

		# server.login(usr, psd)

		for to in tolist:

			msg = MIMEText(content % to["login"], 'html')

			msg["From"] = morf
			msg["To"] = to["email"]
			msg["Subject"] = subject

			try:

				server.sendmail(morf, [to["email"]], msg.as_string())

				print "successfully sent email to %s, addr: %s" % (to["login"], to["email"])

				log.write("successfully sent email to %s, addr: %s\n" % (to["login"], to["email"]))

				time.sleep(300)

			except:

				print "failed to send email to %s, addr: %s" % (to["login"], to["email"])

				log.write("failed to send email to %s, addr: %s\n" % (to["login"], to["email"]))

				continue

		server.close()

		print "successfully sent the mail..."

	except:

		print "failed to send mail..."

	finally:

		log.close()

def get_user_list():

	mongo_client = pymongo.MongoClient('127.0.0.1', 27017)

	msif = mongo_client.msif

	github_users = msif.github_users

	items = github_users.find({}, {"login":1, "email":1, "_id":0})

	items = [ {"login":item["login"], "email":item["email"]} \
			  for item in items \
			  if item.has_key("email") \
			  and item["email"] != None \
			  and item["email"] != '' ]

	# items = reversed(items)

	# seeds = open("GithubUsersEmails.json", 'w')

	# for item in items:

	# 	seeds.write(str(item))

	# 	seeds.write("\n")	

	# seeds.close()

	return items

if __name__ == '__main__':
	
	# argument_parser = argparse.ArgumentParser(description="")

	# argument_parser.add_argument("usr", help="")

	# argument_parser.add_argument("psd", help="")

	# args = argument_parser.parse_args()

	# usr = args.usr
	# psd = args.psd

	user_list = get_user_list()

	# user_list = [{"login":"stamaimer", "email":"stamaimer@gmail.com"},
	# 			 {"login":"stamaimer", "email":"stamaimer@icloud.com"},
	# 			 {"login":"curmium", "email":"hiwiky@gmail.com"},
	# 			 {"login":"yaohu", "email":"kokoroyao@gmail.com"}]

	# sendmail(usr, psd, usr, user_list)

	sendmail(user_list)
