from flask import Blueprint, request
import json

from contracts.v1 import *
from entities import *

bp_crawler = Blueprint('crawler', __name__)

@bp_crawler.route('/', methods=['GET'])
def index():
    return 'bp_crawler index'

@bp_crawler.route('/query', methods=['GET'])
def query_data():
    # TODO: handle the query
    pass

@bp_crawler.route('/insert', methods=['POST'])
def insert_data():
    x = requests.CrawledSocialDataRequest.from_json(json.loads(request.data))
    # TODO: save to db
    return x.serialize()

@bp_crawler.route('/latest', methods=['GET'])
def latest():
    # TODO: return biggest timestamp
    pass