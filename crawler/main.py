from .twitter import TwitterCrawler
from .alpha_vantage import get_stock
from discord import notify, status_update, warning_update, human_required_update

# List of available crawlers to use with the CLI
crawlers = [TwitterCrawler]

""" Basic crawler lifetime: initialization and basic loop """
def start_crawler(crawler_name, options):
    crawler = [c for c in crawlers if str(c) == crawler_name]

    if len(crawler) == 0:
        raise Exception(f"No crawler with the name {crawler_name} is registered")
    
    crawler = crawler[0]    

    crawler = crawlers[crawler](options)
    notify('crawler', status_update(f'Crawler {crawler} started', crawler))

    for data in crawler:
        try:
            crawler.post(data)
        except Exception as ex:
            notify('crawler', human_required_update(f'Crawler {crawler}: {str(ex)}', crawler))
            return

    notify('crawler', warning_update(f'Crawler {crawler} stopped', crawler))
