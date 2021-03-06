# Reddit Sentiment Analysis Dashboard
This web app is currently hosted at **https://redditsentiment.herokuapp.com/.**

This web app utilizes **Django, Reddit's API** and **Google's Cloud Natural Language API** to offer an at-a-glance
overview of a subreddit's overarching sentiment, with detailed statistics for each post and comment.

# Run the project yourself
## Reddit API Keys
As this project takes advantages of Reddit's API, it requires the use of 2 unique API keys and a unique identifier (user agent).
These can be generated by registering a new Reddit app at https://www.reddit.com/prefs/apps.

For privacy purposes, the `api_keys.py` file containing the necessary keys has been ommited from this repository.
This file must be created and placed in the same directory as `praw_reddit_scraper.py`. `api_keys.py` can be recreated as follows:

```
reddit_client_id = 'client id goes here'
reddit_client_secret = 'secret token goes here'
reddit_user_agent = 'your descriptive identifier containing your program name and Reddit username goes here'
```

Note that while the first two API keys are provided by Reddit, the `reddit_user_agent` key **must** be written by yourself, to prevent abuse of the Reddit API.
For example: `'RedditSentimentCrawler v0.1, by /u/UsernameHere'`

## Google Cloud Natural Language API
Queries to Google's Cloud NLP API are also implemented in the project. As such, each time you wish to run the development server locally, the you must set an environment variable linking to your Google Cloud Platform API Key. More information can be found at https://cloud.google.com/natural-language/docs/quickstart-client-libraries.

Note: Only 5000 queries (pieces of text <1000 characters) to each API endpoint (of which sentiment analysis is included) are free, per billing month.

