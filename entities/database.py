from api import db

class CrawledSocialDataEntity(db.Model):
    __tablename__ = 'crawledsocialdataentity'

    cid = db.Column(db.String(255), primary_key=True)
    content = db.Column(db.Text())
    timestamp = db.Column(db.Float())

    def __repr__(self):
        return '<CrawledSocialDataEntity %r>' % self.cid

class CrawledSocialDataEntityTags(db.Model):
    __tablename__ = 'crawledsocialdataentitytags'

    tag = db.Column(db.String(255), primary_key=True)
    cid = db.Column(db.String(255), db.ForeignKey('crawledsocialdataentity.cid'), primary_key=True)

    def __repr__(self):
        return '<CrawledSocialDataEntity %r %r>' % self.tag, self.cid