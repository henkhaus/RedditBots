import praw
import os
import re
import pdb
import secrets

# connect to reddit and create instance
user_agent = 'testing by /u/redditbottesting 0.9.0'

r = praw.Reddit(user_agent=user_agent,
                client_id=secrets.client_id,
                client_secret=secrets.client_secret,
                username=secrets.username,
                password=secrets.password)


if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))


subreddit = r.subreddit('pythonforengineers')
for submission in subreddit.hot(limit=5):
    if submission.id not in posts_replied_to:
        if re.search('i love python s', submission.title, re.IGNORECASE):
            submission.reply("hello")
            print("Bot replying to : ", submission.title)
            posts_replied_to.append(submission.id)


with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")


