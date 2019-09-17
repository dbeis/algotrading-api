from ..common import *
from contracts.v1 import *
import time 
import json
from discord import *

def start_tweet_crawler(config):
    print('\n\n')

    print('Retrieving latest data for progress')
    # step one, fetch progress
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
            latest_data = CrawledSocialDataRecordResponse.from_json(json.loads(r.json()))
            latest_cid = latest_data.cid
        else:
            raise Exception(f'Bad status code {r.status_code}')
    except BaseException as e:
        print(str(e))
        # let this as-is if we are to start crawler processes manually
        # add more handling and discord / service worker notifications if we automate deploying it
        print('Startup failed. Aborting.')
        return
    
    # step two, data fetch-post loop
    while(True):
        print(f'Fetching more twitter data starting from cid {latest_cid}')
        # data fetch ..snip.. (omitted for brevity)
        # include error handling for twitter etc

        # == # map the fetched data to the contracts
        new_data = CrawledSocialDataRequest([
            CrawledSocialDataRecord(
                'cid500',
                'this is the tweet content',
                1.0, # timestamp -- parse that properly so it's unix time
                ['twitter', 'bitcoin'] # example | pass hashtags / search query through config
            )
        ])

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
        latest_cid = new_data.data[-1].cid

        # if reached end of tweets, wait some time till you get new ones (like an hour)
        # ..snip..

        # account for twitter's api usage metering
        # ..snip.. // sleep()

