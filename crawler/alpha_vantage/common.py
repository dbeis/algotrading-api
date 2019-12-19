from alpha_vantage.timeseries import TimeSeries
import os


def init_api_key(apikey = None):
    """
    Checks that the api key exists in the system
    :param apikey: string containing the api key
    :return:
    """
    if apikey:
        os.environ['ALPHAVANTAGE_API_KEY'] = str(apikey)
        return True
    elif 'ALPHAVANTAGE_API_KEY' in os.environ.keys():
        return True
    else:
        raise Exception(f'Api key for Alpha Vantage not given')



def verify_api_key():
    """
    Verifies the api key for Alpha Vantage
    :return:
    """
    init_api_key()
    ts = None
    try:
        ts = TimeSeries(key=os.environ['ALPHAVANTAGE_API_KEY'],treat_info_as_error=False)
    except Exception as ex:
        raise Exception(f'Alpha Vantage key not valid {ex}.')
    if type(ts) == TimeSeries:
        return True
    else:
        raise TypeError(f'Returned type not expected: {type(ts)}')


os.environ['ALPHAVANTAGE_API_KEY'] = 'KDAHGTss3OM2OXC022'
verify_api_key()