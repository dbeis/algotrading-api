from crawler.crawler_base import Crawler
import requests as req
from contracts import *
import time
import json
from discord import *
import requests
import re
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import os
import warnings
import time
from crawler.alpha_vantage.common import init_api_key, verify_api_key
from datetime import datetime

class intradayCrawler(Crawler):


    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.interval_capabilities = ['1min', '5min', '15min', '30min', '60min']
        self.default_interval = '5min'
        # Check that we have an api key
        if 'api_key' in self.config.keys():
            init_api_key(self.config['api_key'])
        else:
            init_api_key()

        # Verify that it works
        verify_api_key()

        # Check the configuration
        if 'interval' not in self.config:
            self.config['interval'] = '1min'
        if self.config['interval'] not in self.interval_capabilities:
            warnings.warn(f'An interval of {self.config["interval"]} is not supported. Using {self.default_interval}')
            self.config['interval'] = self.default_interval

        if 'symbol' not in self.config:
            raise Exception('No symbol specified for the Crawler')


        self.ts = TimeSeries(output_format='json')

        self.base_url = config['base_url'] if 'base_url' in config else 'http://localhost:8080'

    def __getitem__(self, index):

        data, meta_data = self.ts.get_intraday(symbol= self.config['symbol'],
                                             interval=self.config['interval'],
                                             outputsize='full')

        last_refreshed = time.mktime(datetime.strptime(meta_data['3.Last Refreshed'], "%Y-%m-%d %H:%M:%S").timetuple())

        # Todo: check with date time from db and stop iteration?
        dt_object = datetime.fromtimestamp(last_refreshed)


        new_data = EconDataListRequest(self.compile_data(data))
        return new_data

    def post(self, data):
        if data is None:
            return

        try:
            response = req.post(url = self.base_url + '/api/alphavantage_crawler/insert', data=data.serialize())
            if response.status_code != 200:
                # bad request? 404? duplicates? -- only thing that matters is that it is not OK
                # connectivity is not bad because exception was not raised, so no reschedule
                # that should be a dev-only error. Thus, just notify discord
                raise Exception(f'Got not-OK status code {response.status_code}.')
            # success
        except BaseException as e:
            print(str(e))
            notify('crawler', human_required_update(str(e), 'alphavantage'))
            return

    def __str__(self):
        return "Alpha Vantage"


    def datetime_to_timestamp(self, datetime):
        return time.mktime(datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S").timetuple())

    def compile_data(self, data):
        EconData_list = []
        for timestamp_key, values in data.items():
            EconData_list.append(
                EconData(
                    timestamp= self.datetime_to_timestamp(timestamp_key),
                    equity= self.config['symbol'],
                    open_price= values['open'],
                    close_price= values['close'],
                    high_price= values['high'],
                    low_price= values['low'],
                    volume= values['volume'],
                )
            )
        return EconData_list


