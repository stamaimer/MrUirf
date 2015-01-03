import requests
import pymongo
import time
import sys

endpoint = "https://api.github.com/users"

mongo_client = pymongo.MongoClient("127.0.0.1", 27017)

msif = mongo_client.msif

github_users = msif.github_users

def crawl(since):

    response = requests.get(endpoint, params = {"since" : since})

    if 200 == response.status_code:

        print "get %s success" % response.url

        users = response.json()

        for user in users:

            github_users.insert(user)

        time.sleep(60)

        return users

    else:

        print "get %s failure" % response.url

        print response.json()["message"]

def main():

    users = crawl(sys.argv[1])

    while len(users):

        users = crawl(users[len(users) - 1]["id"])

if __name__ == '__main__':

    main()
