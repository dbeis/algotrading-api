import flask
import api
import sys
import json

from contracts.CrawledDataRecord import *
from contracts.CrawledDataRecordList import *
from contracts.EconDataList import EconDataListRequest
from entities import *
from .common import ok, error, not_found
from flask import request


bp_crawler = flask.Blueprint('crawler', __name__)

@bp_crawler.route('/', methods=['GET'])
def index():
    return 'bp_crawler index'

@bp_crawler.route('/query', methods=['GET'])
def query_data():
    page = flask.request.args.get('page', default = 1, type = int)

    pageSize = flask.request.args.get('pageSize', default = 200, type = int) 
    pageSize =  200 if pageSize > 200 else pageSize

    tags = flask.request.args.getlist('tags', default = 1, type = int)
    fromTime = flask.request.args.get('fromTime', default = 0, type = float)
    untilTime = flask.request.args.get('untilTime', default = sys.float_info.max , type = float)

    # validate query params
    
    # query
    
    return ok()

@bp_crawler.route('/insert', methods=['POST'])
def insert_data():
    req = CrawledDataListRequest.from_json(json.loads(flask.request.data))

    if req is None or req.data is None or len(req.data) == 0:
        return json.dumps({ error: ''})
    # validate
    for record in req.data:
        if record is None or record.cid is None or record.content is None or len(record.content) == 0:
            return error()
        if record.tags is None or len(record.tags) < 1:
            return error('Not enough tags') 
        # check max tag count maybe?

    api.db.session.add_all([
        CrawledDataListEntity(cid = x.cid, content = x.content, timestamp = x.timestamp)
        for x in req.data
    ])
    api.db.session.add_all([
        CrawledDataListEntityTags(tag = t, cid = x.cid)
        for x in req.data
        for t in x.tags
    ])

    api.db.session.commit()

    return ok()


@bp_crawler.route('/insert_econ', methods=['POST'])
def insert_econ_data():
    req = EconDataListRequest.from_json(json.loads(flask.request.data))

    if req is None or req.data is None or len(req.data) == 0:
        return json.dumps({ error: ''})
    # validate
    for record in req.data:
        if record is None or record.timestamp is None or record.equity is None:
            return error()
        #=============================================
        #       placeholder
        #=============================================
        
        #if record.tags is None or len(record.tags) < 1:
            #return error('Not enough tags') 
        # check max tag count maybe?

    return ok()


@bp_crawler.route('/latest', methods=['GET'])
def latest():
    r = CrawledDataListEntity.query.order_by(CrawledDataListEntity.timestamp.desc()).limit(1).all()
    if r is None or len(r) == 0:
        return not_found()
    result = r[0]
    print(r[0])
    return ok(CrawledDataResponse(
        cid = result.cid, 
        content = result.content,
        timestamp = result.timestamp,
    ).serialize())