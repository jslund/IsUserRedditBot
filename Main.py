import praw
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime
#logging.basicConfig(level=logging.DEBUG)


CLIENTID=os.getenv('CLIENT_ID')
CLIENTSECRET=os.getenv('CLIENT_SECRET')
CLIENTPASSWORD = os.getenv('CLIENT_PASSWORD')
useragent = "script:IsUser?:v1"

def GetComments(username):

    time = datetime.now()

    user = reddit.redditor(username)

    comment_list = []

    for comment in user.comments.new(limit=None):
        comment_list.append({'body': comment.body, 'author': comment.author.name})

    print("Comments retrieved, taking {} seconds".format(str(datetime.now() - time)))



    return comment_list

def WriteComments(comment_string):
    with open('second_comments.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(comment_string)

def GetSubmissions(username):
    time = datetime.now()

    user = reddit.redditor(username)

    post_list = []

    for post in user.submissions.new():
        if hasattr(post, 'selftext'):
            post_list.append({'body': post.selftext, 'author': post.author.name})

    print("Posts retrieved taking {} seconds".format(str(datetime.now()-time)))

    return post_list

if __name__ == '__main__':

    start_time = datetime.now()

    reddit = praw.Reddit(client_id=CLIENTID,
                         client_secret=CLIENTSECRET,
                         user_agent=useragent,
                         username='IsThisAUserBot',
                         password=CLIENTPASSWORD
                         )


    base_username = input("Input user you think this is: ")

    base_comments = GetComments(base_username)

    base_posts = GetSubmissions(base_username)

    base_comments.extend(base_posts)

    second_username = input("Input user you want to check: ")

    second_comments = GetComments(second_username)

    second_posts = GetSubmissions(second_username)

    second_comments.extend(second_posts)


    number_of_comments = min(len(base_comments), len(second_comments))

    if len(base_comments) > number_of_comments:
        number_to_remove = len(base_comments) - number_of_comments
        while number_to_remove > 0:
            base_comments.pop()
            number_to_remove -= 1
    elif len(second_comments) > number_of_comments:
        number_to_remove = len(second_comments) - number_of_comments
        while number_to_remove > 0:
            second_comments.pop()
            number_to_remove -= 1
    else:
        print("Same Length")


    texts = [comment['body'] for comment in base_comments]
    authors = [comment['author'] for comment in base_comments]
    texts.extend([comment['body'] for comment in second_comments])
    authors.extend([comment['author'] for comment in second_comments])

    time = datetime.now()

    vectorizer = TfidfVectorizer(ngram_range=(1,5), min_df=2)
    vectors = vectorizer.fit_transform(texts)
    print(vectors.shape)

    X_train, X_test, y_train, y_test = train_test_split(vectors, authors, test_size=0.2, random_state=1337)

    svm = LinearSVC()

    try:
        svm.fit(X_train, y_train)
    except ValueError:
        print("You cannot search the same user")

    predictions = svm.predict(X_test)

    accuracy = (accuracy_score(y_test, predictions)*100)

    print("I am {}% sure that {} is not {}".format(str(accuracy), second_username, base_username))

    print("This calculation took {} seconds".format(str(datetime.now()-time)))

    print("Taking {} seconds overall".format(str(datetime.now()-start_time)))

