import os
import pickle
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bus import consume, declare, connect
from dotenv import load_dotenv
from comment import Comment
from processed_comment import ProcessedComment
load_dotenv()

USER = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')

DATABASE_URI= f'mysql+pymysql://{USER}:{PASSWORD}@host.docker.internal/{DB_NAME}'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class RawComment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    fb_comment_id = Column(String(255), unique=True, nullable=False)
    comment = Column(Text, nullable=False)
    user_name = Column(String(255))
    user_id = Column(String(255))
    time = Column(String(255))

class ProcessedComment(Base):
    __tablename__ = 'processed_comments'
    id = Column(Integer, primary_key=True)
    fb_comment_id = Column(String(255), unique=True, nullable=False)
    sentiment = Column(String(50))
    category = Column(String(100))
    sub_category = Column(String(100))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

Base.metadata.create_all(engine)


def save_raw_comment(ch, method, properties, body):
    comment = pickle.loads(body)
    raw_comment = RawComment(
        user_name=comment.user_name,
        user_id=comment.user_id,
        comment=comment.comment,
        time=comment.time,
        fb_comment_id=comment.fb_comment_id
    )
    session.add(raw_comment)
    session.commit()

def save_processed_comment(ch, method, properties, body):
    processed_comment = pickle.loads(body)
    processed = ProcessedComment(
        fb_comment_id=processed_comment.fb_comment_id,
        sentiment=processed_comment.sentiment,
        category=processed_comment.category,
        sub_category=processed_comment.sub_category
    )
    session.add(processed)
    session.commit()

if __name__ == "__main__":
    RABBITHOST = os.getenv('RABBITHOST', 'rabbitmq')
    connection = connect(RABBITHOST)
    while not connection:
        connection = connect(RABBITHOST)

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    declare(['comments', 'processed_comment'], channel)
    
    consume(queue='comments', callback=save_raw_comment, channel=channel)
    consume(queue='processed_comment', callback=save_processed_comment, channel=channel)
