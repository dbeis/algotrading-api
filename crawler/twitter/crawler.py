from ..common import *
from contracts import *
import time 
import json
from discord import *
import requests
from bs4 import BeautifulSoup
import re

# Extract data from a tweets batch
def tweets_from_batch(tweets_batch):
    tweets_soup = BeautifulSoup(tweets_batch, 'html.parser')
    html_tweets = tweets_soup.find_all('li', {'id': re.compile(r'^stream-item-tweet')})
    crawledData_tweets = []
    for html_tweet in html_tweets:
        crawledData_tweets.append(
            CrawledData( 
                html_tweet.get('data-item-id'),
                html_tweet.select_one('li .content .js-tweet-text-container').text,
                html_tweet.select_one('li .time span[data-time]').get('data-time'),
                ['bitcoin']
            )
        )
    
    return crawledData_tweets

def set_headers(headers, url=None):
    # We then set some of them as needed
    if url:
        headers['Referer'] = url # Optional
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' # Optional
    headers['Accept-Language'] = 'en' # Optional
    headers['User-Agent'] = 'TweetScraper' # Mandatory
    headers['Accept-Encoding'] = 'gzip,deflate' # Optional

def start_tweet_crawler(config):
    print('\n\n')
    print('Retrieving latest data for progress')
    # Init config
    session = requests.Session()
    url = config['url'] if 'url' in config and config['url'] else \
        'https://twitter.com/i/search/timeline?l=&f=tweets&q=bitcoin&src=typed&max_position='
    wait_secs = config['wait_secs'] if 'wait_secs' in config and config['wait_secs'] else \
        5 # Minimum 1 sec for scraping fairplay
    min_position = ''
    has_more_items = True

    
    # step one, fetch progress

    # step two, data fetch-post loop
    while(has_more_items):
        #print(f'Fetching more twitter data starting from cid {latest_cid}')
        # data fetch ..snip.. (omitted for brevity)
        # Get headers and add them to next request
        headers = session.cookies.get_dict()
        set_headers(headers, url + min_position)
        
        # Get request (XHR)
        # include error handling for twitter etc
        try:
            response = session.get(url + min_position, headers=headers)    
        except requests.exceptions.Timeout as e:
            print(str(e))
            # if timeout error happens, notify discord
            notify('crawler', warning_update(str(e), 'twitter'))
            continue
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            print(str(e))
            notify('crawler', error_update(str(e), 'twitter'))
            return
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.HTTPError as e:
            print(str(e))
            # if http error, notify discord
            notify('crawler', error_update(str(e), 'twitter'))
            return
        except requests.exceptions.RequestException as e:
            print(str(e))
            notify('crawler', error_update(str(e), 'twitter'))
            return
            # catastrophic error. bail.

        json_response = json.loads(response.content.decode("utf-8"))        
                
        # == # map the fetched data to the contracts
        new_data = CrawledDataListRequest(tweets_from_batch(json_response['items_html']))
        
        # post them to the server
        try:
            response = post_social_data(new_data)
            if response.status_code != 200:
                # bad request? 404? duplicates? -- only thing that matters is that it is not OK
                # connectivity is not bad because exception was not raised, so no reschedule
                # that should be a dev-only error. Thus, just notify discord
                raise Exception(f'Got not-OK status code {response.status_code}.')
            # success
        except BaseException as e:
            print(str(e))
            # if unknown exception happens and we can't automatically recover, notify discord
            notify('crawler', human_required_update(str(e), 'twitter'))
            return

        print(f'Successfully posted tweets cids: {new_data.data[0].cid} ~ {new_data.data[-1].cid}')
        # set up for next iteration
        min_position = json_response['min_position']
        has_more_items = json_response['has_more_items']

        # if reached end of tweets, wait some time till you get new ones (like an hour)
        # ..snip..

        # account for twitter's api usage metering
        # ..snip.. // sleep()
        time.sleep(wait_secs)

