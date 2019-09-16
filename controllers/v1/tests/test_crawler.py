import flask
import controllers.v1.crawler as controller
from contracts.v1 import requests
from controllers.common import ok, error, not_found
from entities import models
import api

def test_insert_data_correct(mocker):   
    # arrange
    data_to_insert = requests.CrawledSocialDataRequest([
        requests.CrawledSocialDataRecord('cid0', 'content0', 123.4, ['tag0', 'tag1']),
        requests.CrawledSocialDataRecord('cid1', 'content1', 123.4, ['tag1', 'tag2'])
    ])

    expected_entities_inserted = [models.CrawledSocialDataEntity(cid = x.cid, content = x.content, timestamp = x.timestamp)
        for x in data_to_insert.data]

    expected_tags_inserted = [models.CrawledSocialDataEntityTags(tag = t, cid = x.cid)
        for x in expected_entities_inserted
        for t in x.tags]

    request_mock = mocker.patch.object(flask, 'request')
    request_mock.data = data_to_insert.serialize()
    db_mock = request_mock = mocker.patch.object(api, 'db')

    # act
    result = controller.insert_data()

    # assert

    db_mock.session.add_all.assert_called_with(*expected_entities_inserted, *expected_tags_inserted)
    db_mock.session.commit.assert_any_call()

    assert result == ok()