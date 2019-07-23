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
    #
    master_submission_data_list = scrape_instance.get_submission_data()
 
    if scrape_instance.sub_exists():
        test_list = ['hi', 'hello', 'hey', 'hiya', 'heyo']

        args = {'subreddit':subreddit, 'subreddit_info':subreddit_info, 'test_list':test_list}
        return render(request, 'analyze_sentiment.html', args)

    '''
    Form validation logic. WIP.
    else:
        form = SubredditForm()
        return render(request, 'index.html', {'subreddit_form': form})
    '''