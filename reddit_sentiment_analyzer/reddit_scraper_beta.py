# Import Reddit API wrapper (PRAW), hidden API keys from api_keys.py for PRAW, and Pushshift API wrapper (PSAW) 
import praw
from api_keys import reddit_client_id, reddit_client_secret, reddit_user_agent
from psaw import PushshiftAPI
import pandas as pd

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Import 'time' module for queries taking date as a parameter
import time

#RANDOM MODULE FOR DEBUGGING
import random

#Create a Google Cloud client instance
google_client = language.LanguageServiceClient()

#PSAW Manager
class PushshiftAPIScraperManager:
    def __init__(self, subreddit, num_posts, sort_type, after_time, before_time):
        # Receive arguments from object
        self.subreddit = subreddit
        self.limit = num_posts
        self.sort_type = sort_type
        self.after_time = after_time
        self.before_time = before_time
        #Initialize list to store dictionaries of submission info
        self.master_submission_data_list = []
        # Configure read-only reddit instance to query API for data
        self.reddit = praw.Reddit(client_id=reddit_client_id,
                                  client_secret=reddit_client_secret,
                                  user_agent=reddit_user_agent)
        # Configure PSAW to use reddit instance created using PRAW
        self.api = PushshiftAPI()

    # scrape_submission_ids and scrape_submission_info are only necessary if the user 
    # wishes to scrape a specific timeframe, rather than just view the current 'hot' posts

    def scrape_submissions(self):
        submissions_data = self.api.search_submissions(subreddit=self.subreddit,
                                                          limit=self.limit,
                                                          sort_type=self.sort_type,
                                                          after=self.after_time,
                                                          filter=['id', 'score', 'title', 'author'],)
                                                          #before=self.before_time-6000)                                       
        return list(submissions_data)

    def process_submissions_data_list(self):
        # Receive unprocessed submissions' data from scrape_submissions
        submissions_data = self.scrape_submissions()
        for submission in submissions_data:
            temp_submission_dict = submission[6]
            '''
            temp_submission_dict at this point has the following keys:
                {'author', 'created_utc', 'id', 'score', title', 'created'}
            1. 'comments' and its corresponding value, comments_list[], will be appended later on in this iteration of the for loop
            2. 'created_utc' and 'created' have duplicate values ('created' key-value will be removed)
            '''
            # Delete duplicate 'created' key-value pair in dictionary
            del temp_submission_dict['created']

            # Each element of comment_list[] is a dictionary for an individual comment.
            # scrape_submission_comments() will handle constructing individual comment dictionaries and storing them in comments_list[]
            comments_list = self.scrape_submission_comments(temp_submission_dict['id'])
            temp_submission_dict['comments'] = comments_list
            # Append temp_submission_dict to master submission data list
            self.master_submission_data_list.append(temp_submission_dict)
        
        #Function returns master list containing all submissions data and their corresponding comments
        return self.master_submission_data_list

    #This function takes a submission's ID as an argument, constructs a dictionary for each top level comment, and stores them in a list (which it returns)
    def scrape_submission_comments(self, submission_id):
        #Initialize comments_list, to store dictionaries of individual comments
        comments_list = []
        # Query Reddit API to create submission instance
        submission_instance = self.reddit.submission(id=submission_id)
        # Following line of code may be modified with: 'top', 'new', or 'controversial'
        submission_instance.comment_sort = 'top'
        submission_instance.comments.replace_more(limit=0)
        
        # Loops through CommentForest pulled from submission_instance and appends each top level comment to comments_list
        for top_level_comment in submission_instance.comments[:20]:
            #Create temporary dictionary for each comment
            temp_comment_data = {}
            #Store comment data in individual temp_comment_data dictionary
            temp_comment_data['text'] = top_level_comment.body
            temp_comment_data['score'] = top_level_comment.score
            temp_comment_data['author'] = top_level_comment.author
            temp_comment_data['created_utc'] = top_level_comment.created_utc
            temp_comment_data['stickied'] = top_level_comment.stickied

            #Calls get_sentiment_score and passes comment text as argument, returns sentiment score
            #FOR DEBUGGING, GENERATE RANDOM NUMBER BETWEEN -1 AND 1 (UNCOMMENT NEXT LINE FOR PRODUCTION)
            #temp_comment_data['sentiment_score'] = self.get_sentiment_score(temp_comment_data['text'])
            temp_comment_data['sentiment_score'] = round(random.uniform(-1,1),2)
            #Append comment's dictionary to comments_list
            comments_list.append(temp_comment_data)

        return comments_list

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

scrape_object = PushshiftAPIScraperManager('politics', 1, 'score', 1562719793, time.time()) #Debugging arguments
print(scrape_object.process_submissions_data_list()[0]['comments'][2]['sentiment_score']) # Debugging
