import bot_class
import markovify


def markov_maker(sub, r, posts_replied_to):

    """reply to a reddit comment given a subreddit, search term, and reply"""
    subreddit = r.subreddit(sub)

    for submission in subreddit.hot(limit=10):
        # see if bot has already replied to the post
        if submission.id not in posts_replied_to:
            submission.comments.replace_more(limit=0)
            comment_text = ''
            print(submission)
            for comment in submission.comments.list():
                comment_text = comment_text+'\n'+comment.body
            if len(submission.comments.list()) > 3:
                text_model = markovify.NewlineText(comment_text)
                if text_model.make_sentence(tries=100) is not None:
                    print(submission.title)
                    print('response ->')
                    print(text_model.make_sentence(tries=100))
                    print('end')
                    #bot.handle_ratelimit(comment.reply, bot.reply_format(palindrome_set))
                    #posts_replied_to.append(submission.id)


if __name__ == '__main__':
    bot = bot_class.RedditBot('mrmarkovbot')
    #print(bot.posts_replied_to)
    markov_maker('running', bot.r, bot.posts_replied_to)
    # this 'kills' the bot
    bot.reply_tracking_pack()