from api import db

class CrawledDataListEntity(db.Model):
    __tablename__ = 'CrawledDataListentity'

    cid = db.Column(db.String(255), primary_key=True)
    content = db.Column(db.Text())
    timestamp = db.Column(db.Float())

    def __repr__(self):
        return '<CrawledDataListEntity {0} {1} {2}>'.format(self.cid, self.content, str(self.timestamp))

    def __eq__(self, other):
        if isinstance(other, CrawledDataListEntity):
            return self.cid == other.cid and \
                self.content == other.content and \
                self.timestamp == other.timestamp
        return False

class CrawledDataListEntityTags(db.Model):
    __tablename__ = 'crawleddatalistentitytags'

    tag = db.Column(db.String(255), primary_key=True)
    cid = db.Column(db.String(255), db.ForeignKey('crawleddatalistentity.cid'), primary_key=True)

    def __repr__(self):
        return '<CrawledDataListEntityTags {0} {1}>'.format(self.tag, self.cid)

    def __eq__(self, other):
        if isinstance(other, CrawledDataListEntity):
            return self.tag == other.tag and self.cid == other.cid
        return False

        