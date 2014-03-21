from sqlalchemy import Column, Integer, String
from cdc_db import Base

class NewsPost(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    heading = Column(String(128))
    body = Column(String(1024))

    def __init__(self, head=None, body=None):
        self.heading = head
        self.body = body

    def __repr__(self):
        return '<News %r>' % (self.heading)
