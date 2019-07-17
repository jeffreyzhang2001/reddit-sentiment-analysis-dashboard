# reddit-sentiment-analysis-dashboard
This web app utilizes **Django, Reddit's API (accessed through Pushshift's API)** and **Google's Cloud Natural Language API** to offer an at-a-glance
breakdown of desired subreddit's overarching sentiment, with detailed statistics for each post and comment.

# Run the project yourself
As this project takes advantages of Reddit's API, it requires the use of 2 unique API keys and a unique identifier (user agent).
These can be generated by registering a new Reddit app at https://www.reddit.com/prefs/apps.

For privacy purposes, the `api_keys.py` file containing the necessary keys has been ommited from this repository.
This file must be created and placed in the same directory as `data_scraper.py`. `api_keys.py` can be recreated as follows:

```
reddit_client_id = 'client id goes here'
reddit_client_secret = 'secret token goes here'
reddit_user_agent = 'your descriptive identifier containing your program name and Reddit username goes here'
```

Note that while the first two API keys are provided by Reddit, the `reddit_user_agent` key **must** be written by yourself, to prevent abuse of the Reddit API.
For example: `'RedditSentimentCrawler v0.1, by /u/UsernameHere'`
 
