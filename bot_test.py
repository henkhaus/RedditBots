import praw
import os
import re
import secrets

# connect to reddit and create instance
user_agent = 'testing by /u/redditbottesting 0.9.0'
r = praw.Reddit(user_agent=user_agent,
                client_id=secrets.client_id,
                client_secret=secrets.client_secret,
                username=secrets.username,
                password=secrets.password)


def reply_tracking_unpack():
    """returns list of posts the bot has already replied to"""
    if os.path.isfile('posts_replied_to.txt'):
        # file exists, read contents into list
        with open('posts_replied_to.txt', 'r') as f:
            post_ids = f.read()
            post_ids = post_ids.split("\n")
            post_ids = list(filter(None, post_ids))
    else:
        # create empty list
        post_ids = []
    return post_ids


def post_reply(sub, search_term, reply):
    """reply to a reddit post given a subreddit, search term, and reply"""
    subreddit = r.subreddit(sub)
    for submission in subreddit.hot(limit=5):
        # see if bot has already replied to the post
        if submission.id not in posts_replied_to:
            if re.search(search_term, submission.title, re.IGNORECASE):
                submission.reply(reply)
                print('Bot replying to : ', submission.title)
                # add post id to list
                posts_replied_to.append(submission.id)


def reply_tracking_pack():
    """take updated list and write to txt"""
    with open('posts_replied_to.txt', 'w') as f:
        for post_id in posts_replied_to:
            f.write(post_id + '\n')


# run it
if __name__ == '__main__':
    posts_replied_to = reply_tracking_unpack()
    post_reply('pythonforengineers', 'i love python s', 'second hello')
    reply_tracking_pack()

