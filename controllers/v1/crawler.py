from flask import Blueprint, request, jsonify
import jsonpickle
import json

from contracts.v1 import *

bp_crawler = Blueprint('crawler', __name__)

@bp_crawler.route('/', methods=['GET'])
def index():
    return 'bp_crawler index'

@bp_crawler.route('/insert', methods=['POST'])
def insert_data():
    x = requests.CrawledSocialDataRequest.from_json(json.loads(request.data))
    return x.serialize()

@bp_crawler.route('/latest', methods=['GET'])
def latest():
    pass