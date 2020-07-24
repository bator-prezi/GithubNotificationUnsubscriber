# GithubNotificationUnsubscriber
Unsubscribe from automatic group pull request review invitations


## How it works
This script run every x seconds and checks if you have new notifications. If you do have, then it checks if it is from a group code review invite. The conditions for this are: the reason of the notification is "review_requested" and you are not directly invited to review the PR.

You won't get unsubscribed if:
* You watch a repo
* You manually subscribed to a PR
* You left a comment on a PR
* You are the author of the PR
* If you interacted with the PR in any way
* In the CODEOWNERS file you are specifically set as the reviewer (and not a group)


## How to run
To run the script you need PyGithub (and also python)
```
pip install PyGithub
```

To run the script create a token.dat file which should contain a Github access token. Make sure the token has rights to private repositories.

After that just run the script:
```
python app.py <update_interval_in_seconds>
```

Works with Python 2 and 3 as well.
