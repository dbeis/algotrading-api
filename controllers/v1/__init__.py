__all__ = ["crawler"]
from .crawler import bp_crawler

def v1_installer(app, prefix):
    app.register_blueprint(bp_crawler, url_prefix=prefix + '/crawler')
