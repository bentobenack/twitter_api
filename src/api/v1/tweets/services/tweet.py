
from sqlalchemy.orm import Session

from api.v1.tweets.models.tweet import Tweet
from api.v1.tweets.schemas.tweet import CreateTweet


# Create a tweet
def create_tweet(db: Session, tweet: CreateTweet):
    
    db_tweet = Tweet(**tweet.dict())
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    
    return db_tweet
    

# Get a tweet
def get_tweet(db: Session, tweet_id: int):
    return db.query(Tweet).filter(Tweet.id == tweet_id).first()


# Get Tweets
def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tweet).offset(skip).limit(limit).all()


# Update a tweet
def update_tweet(db: Session, tweet_id: int, tweet: CreateTweet):
    
    db.query(Tweet).filter(Tweet.id == tweet_id).update(values={**tweet.dict()})
    db.commit()


# Delete a Tweet
def delete_tweet(db: Session, tweet_id: int):
    res = db.query(Tweet).filter(Tweet.id == tweet_id).delete()
    db.commit()
    
    
    