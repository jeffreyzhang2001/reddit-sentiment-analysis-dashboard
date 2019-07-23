from django.shortcuts import render
from .forms import SubredditForm

from .praw_reddit_scraper import RedditScrapeManager

# Create your views here.
def index(request):
    subreddit_form = SubredditForm()
    return render(request, 'index.html', {'subreddit_form' : subreddit_form})

def about(request):
    return render(request, 'about.html')

def analyze_sentiment(request):
    subreddit = request.GET.get('subreddit')
    #Initialize instance of RedditScrapeManager, to call methods on
    scrape_instance = RedditScrapeManager(subreddit)
    #Get subreddit title, subscriber count, and description for banner
    subreddit_info = scrape_instance.get_subreddit_info()
    #Get all submission/comment info
    master_submission_data_list = scrape_instance.get_submission_data()
    #Calculate total average sentiment score from all submissions, and append to subreddit_info dictionary
    subreddit_total_sentiment_score = 0
    subreddit_total_num_comments = 0
    for submission in master_submission_data_list:
        subreddit_total_num_comments += len(submission['comments'])
        subreddit_total_sentiment_score += submission['average_sentiment_score']*(len(submission['comments']))   
    subreddit_average_sentiment_score = subreddit_total_sentiment_score/subreddit_total_num_comments
    subreddit_info['average_sentiment_score'] = round(subreddit_average_sentiment_score,1)

    if scrape_instance.sub_exists():
        args = {'subreddit':subreddit, 'subreddit_info':subreddit_info, 'master_submission_data_list':master_submission_data_list}
        return render(request, 'analyze_sentiment.html', args)

    '''
    Form validation logic. WIP.
    else:
        form = SubredditForm()
        return render(request, 'index.html', {'subreddit_form': form})
    '''