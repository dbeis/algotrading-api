from .twitter_crawler import bp_twitter_crawler
from api import app

def installer(prefix):
    app.register_blueprint(bp_twitter_crawler, url_prefix=prefix + '/twitter_crawler') # /api/crawler .. bla bla

def install_controllers(prefix):
    installer(prefix)
    