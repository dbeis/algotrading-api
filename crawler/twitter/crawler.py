from crawler.crawler_base import Crawler
import requests as req
from contracts import *
import time 
from discord import *
import requests
from bs4 import BeautifulSoup
import re


class TwitterCrawler(Crawler):
    def __init__(self, config):
        self.config = config

        print('\n\n')
        print('Retrieving latest data for progress')
        # Init config
        self.session = requests.Session()
        self.url = config['url'] if 'url' in config and config['url'] else \
            'https://twitter.com/i/search/timeline?l=&f=tweets&q=bitcoin&src=typed&max_position='
        self.wait_secs = int(config['wait_secs']) if 'wait_secs' in config and config['wait_secs'] else \
            5 # Minimum 1 sec for scraping fairplay
        self.min_position = ''
        self.has_more_items = True
        self.base_url = config['base_url'] if 'base_url' in config else 'http://localhost:8080'
    
    def __getitem__(self, index):
        if not self.has_more_items:
            raise StopIteration(f"No more data to scrape. Last scraped tweet: {self.min_position}")
        
        if not self.min_position == '': # if not first request
            time.sleep(self.wait_secs)

        headers = self.session.cookies.get_dict()
        self.set_headers(headers, self.url + self.min_position)
        
        try:
            response = self.session.get(self.url + self.min_position, headers=headers)    
        except requests.exceptions.Timeout as e:
            print(str(e))
            # timeout
            notify('crawler', warning_update(str(e), 'twitter'))
            raise StopIteration(str(e)) # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            print(str(e))
            notify('crawler', error_update(str(e), 'twitter'))
            raise StopIteration(str(e)) # Bad URL. Try a different one.
        except requests.exceptions.HTTPError as e:
            print(str(e))
            notify('crawler', error_update(str(e), 'twitter'))
            raise StopIteration(str(e))
        except requests.exceptions.RequestException as e:
            notify('crawler', error_update(str(e), 'twitter'))
            raise StopIteration(str(e))

        self.json_response = json.loads(response.content.decode("utf-8"))        
                
        # set up for next iteration
        self.min_position = self.json_response['min_position']
        self.has_more_items = self.json_response['has_more_items']

        new_data = CrawledTwitterDataListRequest(self.tweets_from_batch(self.json_response['items_html']))

        return new_data

    def post(self, data):
        if data is None:
            return

        try:
            response = req.post(url = self.base_url + '/api/twitter_crawler/insert', data=data.serialize())
            if response.status_code != 200:
                # bad request? 404? duplicates? -- only thing that matters is that it is not OK
                # connectivity is not bad because exception was not raised, so no reschedule
                # that should be a dev-only error. Thus, just notify discord
                raise Exception(f'Got not-OK status code {response.status_code}.')
            # success
        except BaseException as e:
            print(str(e))
            notify('crawler', human_required_update(str(e), 'twitter'))
            return

        print(f'Successfully posted tweets cids: {data.data[0].cid} ~ {data.data[-1].cid}')

    def __str__(self):
        return "twitter"

    # Extract data from a tweets batch
    def tweets_from_batch(self, tweets_batch):
        tweets_soup = BeautifulSoup(tweets_batch, 'html.parser')
        html_tweets = tweets_soup.find_all('li', {'id': re.compile(r'^stream-item-tweet')})
        crawledData_tweets = []
        for html_tweet in html_tweets:
            crawledData_tweets.append(
                CrawledData(
                    html_tweet.get('data-item-id'),
                    html_tweet.select_one('li .content .js-tweet-text-container').text,
                    int(html_tweet.select_one('li .time span[data-time]').get('data-time')),
                    ['bitcoin']
                )
            )

        return crawledData_tweets

    def set_headers(self, headers, url=None):
        # We then set some of them as needed
        if url:
            headers['Referer'] = url # Optional
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' # Optional
        headers['Accept-Language'] = 'en' # Optional
        headers['User-Agent'] = 'TweetScraper' # Mandatory
        headers['Accept-Encoding'] = 'gzip,deflate' # Optional
