from api import db

class CrawledSocialDataEntity(db.Model):
    __tablename__ = 'crawledsocialdataentity'

    cid = db.Column(db.String(255), primary_key=True)
    content = db.Column(db.Text())
    timestamp = db.Column(db.Float())

    def __repr__(self):
        return '<CrawledSocialDataEntity {0} {1} {2}>'.format(self.cid, self.content, str(self.timestamp))

    def __eq__(self, other):
        if isinstance(other, CrawledSocialDataEntity):
            return self.cid == other.cid and \
                self.content == other.content and \
                self.timestamp == other.timestamp
        return False

class CrawledSocialDataEntityTags(db.Model):
    __tablename__ = 'crawledsocialdataentitytags'

    tag = db.Column(db.String(255), primary_key=True)
    cid = db.Column(db.String(255), db.ForeignKey('crawledsocialdataentity.cid'), primary_key=True)

    def __repr__(self):
        return '<CrawledSocialDataEntityTags {0} {1}>'.format(self.tag, self.cid)

    def __eq__(self, other):
        if isinstance(other, CrawledSocialDataEntity):
            return self.tag == other.tag and self.cid == other.cid
        return False

        