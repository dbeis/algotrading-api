from api import db


class CrawledTwitterDataListEntity(db.Model):
    __tablename__ = 'CrawledTwitterDataListEntity'

    cid = db.Column(db.String(255), primary_key=True)
    content = db.Column(db.Text())
    timestamp = db.Column(db.Integer())

    def __repr__(self):
        return '<CrawledTwitterDataListEntity {0} {1} {2}>'.format(self.cid, self.content, str(self.timestamp))

    def __eq__(self, other):
        if isinstance(other, CrawledTwitterDataListEntity):
            return self.cid == other.cid and \
                self.content == other.content and \
                self.timestamp == other.timestamp
        return False


class CrawledTwitterDataListEntityTags(db.Model):
    __tablename__ = 'CrawledTwitterDataListEntityTags'

    tag = db.Column(db.String(255), primary_key=True)
    cid = db.Column(db.String(255), db.ForeignKey('CrawledTwitterDataListEntity.cid'), primary_key=True)

    def __repr__(self):
        return '<CrawledDataListEntityTags {0} {1}>'.format(self.tag, self.cid)

    def __eq__(self, other):
        if isinstance(other, CrawledTwitterDataListEntity):
            return self.tag == other.tag and self.cid == other.cid
        return False
