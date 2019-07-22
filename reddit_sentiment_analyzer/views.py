from django.shortcuts import render
from .forms import SubredditForm

# Create your views here.
def index(request):
    subreddit_form = SubredditForm()
    return render(request, 'index.html', {'subreddit_form':subreddit_form})

def about(request):
    return render(request, 'about.html')

def analyze_sentiment(request):
    subreddit = request.GET.get('subreddit')
    return render(request, 'analyze_sentiment.html', {'subreddit':subreddit})