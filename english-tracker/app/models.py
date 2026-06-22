from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    theory = Column(Text)
    prompt = Column(Text)
    created_at = Column(DateTime)


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    content = Column(Text)
    status = Column(String)
    created_at = Column(DateTime)
    next_review_date = Column(Date)
    interval_days = Column(Integer)
    review_count = Column(Integer)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(Integer, nullable=False)
    review_date = Column(Date)
    interval_days = Column(Integer)
