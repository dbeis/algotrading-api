import flask
import api

from contracts.CrawledTwitterDataRecordList import *
from contracts.CrawledTwitterDataRecordList import *

from entities import *
from .common import ok, error, not_found

bp_twitter_crawler = flask.Blueprint('twitter_crawler', __name__)


@bp_twitter_crawler.route('/', methods=['GET'])
def index():
    return 'bp_crawler index'


@bp_twitter_crawler.route('/query', methods=['GET'])
def query_data():
    page = flask.request.args.get('page', default=1, type=int)

    page_size = flask.request.args.get('pageSize', default=200, type=int)
    page_size = 5000 if page_size > 5000 else page_size

    tags = flask.request.args.getlist('tags', default=None, type=int)
    from_time = flask.request.args.get('fromTime', default=None, type=float)
    until_time = flask.request.args.get('untilTime', default=None, type=float)

    if tags is None or len(tags) == 0:
        return error("No tags specified")

    if len(tags) > 3:
        return error("Tag count should not exceed 3.")

    query = CrawledTwitterDataListEntity.query

    # query based on time
    if from_time is not None:
        query = query.filter(CrawledTwitterDataListEntity.timestamp >= from_time)
    if until_time is not None:
        query = query.filter(CrawledTwitterDataListEntity.timestamp <= until_time)

    # query based on tags
    for tag in tags:
        query = query.join(CrawledTwitterDataListEntityTags).filter(CrawledTwitterDataListEntityTags.tag == tag)

    result = query.order_by(CrawledTwitterDataListEntity.timestamp.asc()).limit(page_size).offset(page_size * page).items

    if result.total == 0:
        return not_found()

    r = result.items

    return ok(CrawledTwitterDataListResponse(list(map(lambda x: CrawledTwitterDataResponse(
        cid=x.cid,
        content=x.content,
        timestamp=x.timestamp
    ), r))).serialize())


@bp_twitter_crawler.route('/insert', methods=['POST'])
def insert_data():
    req = CrawledTwitterDataListRequest.from_json(json.loads(flask.request.data))

    if req is None or req.data is None or len(req.data) == 0:
        return json.dumps({error: ''})

    for record in req.data:
        if record is None or record.cid is None or record.content is None or len(record.content) == 0:
            return error()
        if record.tags is None or len(record.tags) < 1:
            return error('Not enough tags')

    api.db.session.add_all([
        CrawledTwitterDataListEntity(cid=x.cid, content=x.content, timestamp=x.timestamp)
        for x in req.data
    ])
    api.db.session.add_all([
        CrawledTwitterDataListEntityTags(tag=t, cid=x.cid)
        for x in req.data
        for t in x.tags
    ])

    api.db.session.commit()

    return ok()


@bp_twitter_crawler.route('/latest', methods=['GET'])
def latest():
    r = CrawledTwitterDataListEntity.query.order_by(CrawledTwitterDataListEntity.timestamp.desc()).limit(1).all()
    if r is None or len(r) == 0:
        return not_found()

    result = r[0]
    return ok(CrawledTwitterDataResponse(
        cid=result.cid,
        content=result.content,
        timestamp=result.timestamp,
    ).serialize())
