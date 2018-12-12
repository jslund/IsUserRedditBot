import Main
import os, praw, sys, logging
logging.DEBUG

CLIENTID = os.getenv('CLIENT_ID')
CLIENTSECRET = os.getenv('CLIENT_SECRET')
CLIENTPASSWORD = os.getenv('CLIENT_PASSWORD')
DESIRED_SUBREDDIT = os.getenv('DESIRED_SUBREDDIT')
useragent = "script:IsUser?:v1"

if __name__ == '__main__':
    reddit = praw.Reddit(client_id=CLIENTID,
                         client_secret=CLIENTSECRET,
                         user_agent=useragent,
                         username='IsThisAUserBot',
                         password=CLIENTPASSWORD
                         )

    subreddit = reddit.subreddit(DESIRED_SUBREDDIT)
    for comment in subreddit.stream.comments():
        if '!IsUser' in comment.body:
            valid_comment = comment
            valid_comment.refresh()
            children = valid_comment.replies
            if "IsThisAUserBot" not in [child_comment.author.name for child_comment in children ]:

                try:
                    comment_body = valid_comment.body
                    second_username = comment_body.replace("!IsUser", "")
                    second_username = second_username.replace(" ", "")

                    parent = valid_comment.parent()
                    parent_username = parent.author.name
                    result = Main.PrimaryFunction(parent_username,second_username)
                    comment.reply(result)
                except:
                    print("Unexpected!: ", sys.exc_info()[0])
