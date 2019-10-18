from ..common import *
from contracts import *
import time 
import json
from discord import *
import requests
from bs4 import BeautifulSoup
import re

# Extract data from a tweets batch
def tweetsFromBatch(tweets_batch):
    tweets_soup = BeautifulSoup(tweets_batch, 'html.parser')
    html_tweets = tweets_soup.find_all('li', {'id': re.compile(r'^stream-item-tweet')})
    crawledData_tweets = []
    for html_tweet in html_tweets:
        CrawledData_tweets.append(
            CrawledData( 
                html_tweet.get('data-item-id'),
                tweet_content = html_tweet.select_one('li .content .js-tweet-text-container').text,
                tweet_timestamp = html_tweet.select_one('li .time span[data-time]').get('data-time'),
                ['bitcoin']
            )
        )
    
    return crawledData_tweets

# Set headers as needed
def setHeaders(headers, url=None):
    # headers param includes those returned from the previous request
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
    interval_secs = 5
    url = 'https://twitter.com/i/search/timeline?l=&f=tweets&q=bitcoin&src=typed&max_position='
    min_position = ''
    has_more_items = True
    min_position = ''
    
    # step one, fetch progress
    '''
    latest_data = None
    latest_cid = None
    try:
        r = fetch_social_progress()
        if r.status_code == 404:
            # first time that this boots, with no data on the db
            latest_cid = 'cid0' # fill this properly with the first tweet we want
            print(f'Database is empty. Starting from cid: {latest_cid}')
        elif r.status_code == 200:
            print(r.json())
            latest_data = CrawledDataResponse.from_json(json.loads(r.json()))
            latest_cid = latest_data.cid
        else:
            raise Exception(f'Bad status code {r.status_code}')
    except BaseException as e:
        print(str(e))
        # let this as-is if we are to start crawler processes manually
        # add more handling and discord / service worker notifications if we automate deploying it
        print('Startup failed. Aborting.')
        return
    '''
    
    # step two, data fetch-post loop
    while(has_more_items):
        print(f'Fetching more twitter data starting from cid {latest_cid}')
        # data fetch ..snip.. (omitted for brevity)
        # Get headers and add them to next request
        headers = session.cookies.get_dict()
        setHeaders(headers, url + min_position)
        
        # Get request (XHR)
        # include error handling for twitter etc
        try:
            response = session.get(url + min_position, headers=headers)    
        except requests.exceptions.Timeout:
            raise
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            raise
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.HTTPError as err:
            raise
        except requests.exceptions.RequestException as err:
            raise
            # catastrophic error. bail.

        
        json_response = json.loads(response.content.decode("utf-8"))        
        
        # == # map the fetched data to the contracts
        new_data = CrawledDataListRequest(tweetsFromBatch(json_response['items_html']))

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

        # if reached end of tweets, wait some time till you get new ones (like an hour)
        # ..snip..

        # account for twitter's api usage metering
        # ..snip.. // sleep()
        time.sleep(has_more_items)

