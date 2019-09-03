from flask import Blueprint

bp_crawler = Blueprint('crawler', __name__)

@bp_crawler.route('/')
def index():
    return 'bp_crawler index'