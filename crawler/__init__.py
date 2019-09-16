__all__ = ['common', 'twitter']

from .twitter import start_tweet_crawler

# Registry of available crawlers
crawlers = {
    'twitter': start_tweet_crawler
}

available_crawlers = crawlers.keys()

def start_crawler(crawler, options):
    crawlers[crawler](options)