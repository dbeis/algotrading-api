from .twitter import TwitterCrawler
from discord import notify, status_update, warning_update, human_required_update

# List of available crawlers to use with the CLI
crawlers = [TwitterCrawler]


""" Basic crawler lifetime: initialization and basic loop """
def start_crawler(crawler_name, options):
    crawler = [c for c in crawlers if c.__name__ == crawler_name]

    if len(crawler) == 0:
        raise Exception(f"No crawler with the name {crawler_name} is registered")
    
    crawler = crawler[0]    

    crawler = crawler(options)
    notify('crawler', status_update(f'Crawler {crawler_name} started', crawler_name))

    for data in crawler:
        try:
            crawler.post(data)
        except Exception as ex:
            notify('crawler', human_required_update(f'Crawler {crawler_name}: {str(ex)}', crawler_name))
            return

    notify('crawler', warning_update(f'Crawler {crawler_name} stopped', crawler_name))
