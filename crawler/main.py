from .twitter import start_tweet_crawler
from discord import notify, status_update, warning_update

# Registry of available crawlers
crawlers = {
    'twitter': start_tweet_crawler
}

available_crawlers = crawlers.keys()

def start_crawler(crawler, options):
    notify('crawler', status_update(f'Crawler started', crawler))
    crawlers[crawler](options)
    notify('crawler', warning_update(f'Crawler stopped', crawler))
