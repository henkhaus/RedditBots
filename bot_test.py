import praw
import os
import re
import secrets
import palindrome
import reply_format

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
                print('Bot replying to submission: ', submission.title)
                # add post id to list
                posts_replied_to.append(submission.id)


def comment_reply(sub, search_term, reply):
    """reply to a reddit comment given a subreddit, search term, and reply"""
    subreddit = r.subreddit(sub)
    for submission in subreddit.hot(limit=5):
        # see if bot has already replied to the post
        if submission.id not in posts_replied_to:
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if search_term.lower() in comment.body:
                    comment.reply(reply)
                    print('Bot replying to : ', submission.title)
                    # add post id to list
                    posts_replied_to.append(submission.id)


def palindrome_finder(sub):
    # TODO: need to add functionality to find multiple palindromes in one comment
    """reply to a reddit comment given a subreddit, search term, and reply"""
    subreddit = r.subreddit(sub)
    for submission in subreddit.hot(limit=10):
        # see if bot has already replied to the post
        if submission.id not in posts_replied_to:
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                for word in palindrome.comment_parse(comment.body):
                    if str(palindrome.is_palindrome(word)) == 'True':
                        # found palindrome, post reply with formatting
                        comment.reply(reply_format.add_links(word+'. You made a palindrome!'))
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
    # post_reply('pythonforengineers', 'i love python s', 'second hello')
    # comment_reply('pythonforengineers', 'second hello', 'third')
    palindrome_finder('pythonforengineers')
    reply_tracking_pack()

