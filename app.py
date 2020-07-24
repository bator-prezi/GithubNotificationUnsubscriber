from github import Github
import datetime
import time
import sys

def read_last_update():
	try:
		f = open("last_update.dat", "r")
		time = f.read()
		last_update = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
		f.close()
		return last_update
	except:
		print("No last update time")

	return datetime.datetime.now()

def read_token():
	try:
		f = open("token.dat", "r")
		token = f.read()
		f.close()
		return token.rstrip("\n")
	except:
		print("Error: no access token provided in token.dat")
		exit(-1)

def write_last_update(date):
	try:
		f = open("last_update.dat", "w")
		f.write(date.strftime("%Y-%m-%dT%H:%M:%SZ"))
		f.close()
	except:
		print("Could not write last update time")

def update_timestamp(date):
	date = datetime.datetime.now(date)
	write_last_update(date)

def should_unsubscribe(pr, my_user_id):
	if pr.user.id == my_user_id:
		return False
	requests = pr.get_review_requests()
	for request in requests:
		for user in request:
			if user.id == my_user_id:
				return False
	
	return True


def unsubscribe_from_threads(github):
	previous_update = read_last_update()
	last_notification = previous_update

	print("Getting notifications from " + previous_update.strftime("%Y-%m-%dT%H:%M:%SZ"))
	user = github.get_user()
	print(user.id)
	notis = user.get_notifications(all=True, since=previous_update)
	print("Number of new notifications: " + str(notis.totalCount))
	for noti in notis:
		if noti.reason == "review_requested" and noti.subject.type == "PullRequest":
			if should_unsubscribe(noti.get_pull_request(), user.id):
				print("Unsubscribing from: " + noti.url)
				noti._requester.requestJsonAndCheck("DELETE", noti.subscription_url,)
				last_notification = max(last_notification, noti.updated_at)

	write_last_update(last_notification)

try:
	update_time = int(sys.argv[1])
except:
	update_time = 60
	print("No update interval given, defaulting to 60 seconds")

token = read_token()

while True:
	github = Github(token)
	unsubscribe_from_threads(github)
	time.sleep(update_time)
