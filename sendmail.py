import smtplib
import pymongo
import argpaarse

addr = "smtp.gmail.com"
port = 587

morf = "mr.uir.uif@gmail.com"

tolist = []

subject = ""

content = ""

def sendmail(usr, psd, morf, tolist, subject, content):

	msg = "From: %s\n \
		   To: %s\n \
		   Subject: %s\n \
		   \n \
		   %s" % (morf, ", ".join(tolist), subject, content)

	try:

		server = smtplib.SMTP(addr, port)

		server.ehlo()

		server.starttls()

		server.login(usr, psd)

		server.sendmail(morf, tolist, msg)

		server.close()

		print "successfully sent the mail..."

	except:

		print "failed to send mail..."

		raise

def get_tolist():

	mongo_client = pymongo.MongoClient('127.0.0.1', 27017)

	msif = mongo_client.msif

	github_users = msif.github_users

	items = github_users.find({}, {"login":1, "email":1, "_id":0})

	print type(items[0]), items[0]

	return list(items)

if __name__ == '__main__':
	
	argument_parser = argparse.ArgumentParser(description="")

	argument_parser.add_argument("usr", help="")

	argument_parser.add_argument("psd", help="")

	args = argument_parser.parse_args()

	usr = args.usr
	psd = args.psd

	tolist = get_tolist()

	sendmail(usr, psd, morf, tolist, subject, content)