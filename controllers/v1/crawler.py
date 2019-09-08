from flask import Blueprint, request, jsonify
from contracts.v1 import *
from entities import *
from api import db

from ..common import ok, error, not_found

import sys
import json

bp_crawler = Blueprint('crawler', __name__)

@bp_crawler.route('/', methods=['GET'])
def index():
    return 'bp_crawler index'

@bp_crawler.route('/query', methods=['GET'])
def query_data():
    page = request.args.get('page', default = 1, type = int)

    pageSize = request.args.get('pageSize', default = 200, type = int) 
    pageSize =  200 if pageSize > 200 else pageSize

    tags = request.args.getlist('tags', default = 1, type = int)
    fromTime = request.args.get('fromTime', default = 0, type = float)
    untilTime = request.args.get('untilTime', default = sys.float_info.max , type = float)

    # validate query params
    
    # query
    
    return ok()

@bp_crawler.route('/insert', methods=['POST'])
def insert_data():
    req = requests.CrawledSocialDataRequest.from_json(json.loads(request.data))

    if req is None or req.data is None or len(req.data) == 0:
        return json.dumps({ error: ''})
    # validate
    for record in req.data:
        if record is None or record.cid is None or record.content is None or len(record.content) == 0:
            return error()
        if record.tags is None or len(record.tags) < 1:
            return error('Not enough tags') 
        # check max tag count maybe?

    db.session.add_all([
        models.CrawledSocialDataEntity(cid = x.cid, content = x.content, timestamp = x.timestamp)
        for x in req.data
    ])
    db.session.add_all([
        models.CrawledSocialDataEntityTags(tag = t, cid = x.cid)
        for x in req.data
        for t in x.tags
    ])

    db.session.commit()

    return ok()


@bp_crawler.route('/latest', methods=['GET'])
def latest():
    r = models.CrawledSocialDataEntity.query.order_by(model.CrawledSocialDataEntity.timestamp.desc()).limit(1).all()

    if r is None or len(r) == 0:
        return not_found()
    
    result = r[0]

    return responses.CrawledSocialDataRecordResponse(
        cid = result.cid, 
        content = result.content,
        timestamp = result.timestamp,
    ).serialize()