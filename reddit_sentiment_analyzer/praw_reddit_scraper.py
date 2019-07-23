# Import Reddit API wrapper (PRAW) and hidden API keys from api_keys.py for PRAW
import praw
from .api_keys import reddit_client_id, reddit_client_secret, reddit_user_agent

# Import NotFound to validate subreddit form
from prawcore import NotFound

# Import time modules for UTC to local timezone conversion
import time

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Create a Google Cloud client instance
google_client = language.LanguageServiceClient()

# PRAW Manager class
class RedditScrapeManager:
    def __init__(self, subreddit):
        # Receive arguments from object
        self.subreddit = subreddit
        # Initialize list to store dictionaries of submission info
        self.master_submission_data_list = []
        # Configure read-only reddit instance to query API for data
        self.reddit = praw.Reddit(client_id=reddit_client_id,
                                  client_secret=reddit_client_secret,
                                  user_agent=reddit_user_agent)

        # Create subreddit instance to pass on to class methods
        self.subreddit_instance = self.reddit.subreddit(self.subreddit)

    # Validates existence of subreddit
    def sub_exists(self):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(self.subreddit, exact=True)
        except NotFound:
            exists = False
        return exists

    def get_subreddit_info(self):
        #Initialize empty dictionary to store subreddit information
        subreddit_info = {}
        # Store subreddit data in subreddit_info
        subreddit_info['title'] = self.subreddit_instance.title
        subreddit_info['public_description'] = self.subreddit_instance.public_description
        subreddit_info['subscribers'] = self.subreddit_instance.subscribers
        return subreddit_info

    def get_submission_data(self):
        for submission in self.subreddit_instance.hot(limit=6):
            # Will not scrape stickied posts
            if submission.stickied:
                continue
            else:
                # Initialize temporary dictionary to store submission data
                temp_submission_dict = {}
                temp_submission_dict['title'] = submission.title
                temp_submission_dict['author'] = submission.author
                temp_submission_dict['score'] = submission.score
                temp_submission_dict['upvote_ratio'] = submission.upvote_ratio*100
                temp_submission_dict['timestamp'] = time.strftime("%I:%M %p on %d %B", time.localtime(submission.created_utc))
                temp_submission_dict['url'] = submission.url
                # Process comment data by storing comments in comment_forest and calling get_comment_data on it
                # Following line of code may be modified with: 'top', 'new', or 'controversial'
                submission.comment_sort = 'top'
                submission.comments.replace_more(limit=0)
                comment_forest = submission.comments[:6]
                # comment_data is a dictionary containing a submissions average sentiment score in 'average_sentiment_score' and 'comments_list'
                comment_data = self.get_comment_data(comment_forest)
                temp_submission_dict['comments'] = comment_data['comments_list']
                #Calculate submissions's average sentiment score from its comments
                temp_submission_dict['average_sentiment_score'] = comment_data['average_sentiment_score']
                # Append temp_submission_dict to master_submission_data_list
                self.master_submission_data_list.append(temp_submission_dict)

        return self.master_submission_data_list
    
    def get_comment_data(self, comment_forest):
        # Initialize 'comments_list[]', a list of dictionaries, each storing an individual comment's data
        comments_list = []
        #Initalize total_sentiment_score, to calculate an average from
        total_sentiment_score = 0
        # Loops through comment_forest taken as argument and appends each top level comment to comments_list
        for top_level_comment in comment_forest:
            # Will not scrape stickied comments (usually AutoModerator, or meta posts) or comments longer than 950 characters (cost purposes)
            if top_level_comment.stickied or len(top_level_comment.body) > 950:
                continue
            else:
                # Create temporary dictionary for each comment
                temp_comment_data = {}
                # Store comment data in individual temp_comment_data dictionary
                temp_comment_data['text'] = top_level_comment.body
                temp_comment_data['author'] = top_level_comment.author
                temp_comment_data['score'] = top_level_comment.score
                temp_comment_data['timestamp'] = time.strftime("%I:%M %p on %d %B", time.localtime(top_level_comment.created_utc))
                temp_comment_data['stickied'] = top_level_comment.stickied

                # Calls get_sentiment_score and passes comment text as argument, returns sentiment score
                # NEXT LINE QUERIES GOOGLE CLOUD API (UNCOMMENT NEXT LINE FOR PRODUCTION)
                temp_comment_data['sentiment_score'] = (self.get_sentiment_score(temp_comment_data['text']))*100
                total_sentiment_score += temp_comment_data['sentiment_score']
                # Append comment's dictionary to comments_list
                comments_list.append(temp_comment_data)
            
        #Calculate average sentiment score for the submission
        average_sentiment_score = total_sentiment_score/(len(comments_list))
        return {'comments_list':comments_list, 'average_sentiment_score':average_sentiment_score}

    #Function queries Google Cloud's Natural Language API for each commment
    def get_sentiment_score(self, comment_text):
        #Query API and store value in sentiment_score 
        document = types\
                .Document(content=comment_text,
                        type=enums.Document.Type.PLAIN_TEXT)

        sentiment_score = google_client\
                        .analyze_sentiment(document=document)\
                        .document_sentiment\
                        .score
        
        #Round sentiment score to 2 decimal places
        sentiment_score = round(sentiment_score, 2)
        
        return sentiment_score
