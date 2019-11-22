from .crawler import bp_crawler
from api import app

def installer(prefix):
    app.register_blueprint(bp_crawler, url_prefix=prefix + '/crawler') # /api/crawler .. bla bla

def install_controllers(prefix):
    installer(prefix)
    