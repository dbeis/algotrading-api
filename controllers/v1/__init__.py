__all__ = ["crawler"]
from .crawler import bp_crawler
from api import app

def v1_installer(prefix):
    app.register_blueprint(bp_crawler, url_prefix=prefix + '/crawler') # /api/v1/crawler .. bla bla
