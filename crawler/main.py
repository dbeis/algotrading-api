from .twitter import start_tweet_crawler
from .alpha_vantage import get_stock
from discord import notify, status_update, warning_update

# Registry of available crawlers
crawlers = {
    'twitter': start_tweet_crawler,
    'alpha_vantage' : get_stock
}

available_crawlers = crawlers.keys()

def start_crawler(crawler, options):
    notify('crawler', status_update(f'Crawler started', crawler))
    crawlers[crawler](options)
    notify('crawler', warning_update(f'Crawler stopped', crawler))
