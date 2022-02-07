
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from core.schemas.tweet import CreateTweet, TweetOut, BaseTweet
from core.config.dependency import get_db
from core.crud import tweet as tweet_crud



tweet = APIRouter()

#Create a tweet
@tweet.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    tags=["Tweets"],
    response_model=TweetOut,
    summary="Create a Tweet"
)
def create_tweet(
    tweet: CreateTweet = Body(...),
    db: Session = Depends(get_db)
):
    """
    Creates a tweet
    
    This path operation creates a new tweet in the app.
    
    Parameters:
    - Request body parameters:
        - tweet: **BaseTweet**
        
    Returns a json with the tweet information:
    
    - id: **int**
    - content: **str**
    - user_id: **int**
    - created_at: **datetime**
    - updated_at: **datetime**
    """
    
    return tweet_crud.create_tweet(db, tweet)
   


# Get All Tweets
@tweet.get(
    path="/",
    tags=["Tweets"],
    summary="Get all Tweets",
    response_model=List[TweetOut],
    status_code=status.HTTP_200_OK,
    
)
def get_all_Tweets(
    skip: Optional[int] = Query(default=0),
    limit: Optional[int] = Query(default=100),
    db: Session = Depends(get_db)
):
    """
    Get All Tweets
    
    This path operation shows all Tweets in the app.
    
    Parameters:
        - 
        
    Returns a list of json object with the tweet information:
    
    - id: **int**
    - content: **str**
    - user: **UserOut**
    - created_at: **datetime**
    - updated_at: **datetime**
    """
    
    tweets = tweet_crud.get_tweets(db, skip, limit)
    
    return tweets


# Get a tweet
@tweet.get(
    path="/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    response_model=TweetOut,
    summary="Get a Tweet"
)
def get_tweet(
    tweet_id: int = Path(
        ...,
        gt=0,
        title=" ID",
        description="The tweet ID you want to get",
        example=1
    ),
    db: Session = Depends(get_db)
):
    """
    Get tweet
        
    This path operation allows to get the information of a specific tweet.
    
    Parameters:
    - Path parameters:
        - id: **str**
        
    Returns a json with the tweet information:
    
    - id: **int**
    - content: **str**
    - user: **UserOut**
    - created_at: **datetime**
    - updated_at: **datetime**
    """
    
    db_tweet = tweet_crud.get_tweet(db, tweet_id)
    
    if db_tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
        
    return db_tweet


# Update a tweet
@tweet.put(
    path="/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    response_model=TweetOut
)
def update_tweet(
    tweet_id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID you want to update",
        example=1
    ),
    tweet: BaseTweet = Body(...),
    db: Session = Depends(get_db)
):
    """
    Update a tweet
    
    This path operation allow to update the content of a specific tweet.
    Only the tweet owner can update the tweet.
    
    Parameters:
    - Path parameters:
        - id: **int**
    - Body parameters:
        - tweet: **BaseTweet**
        
    Returns a json with the updated tweet information:
    - id: **int**
    - content: **str**
    - created_at: **datetime**
    - updated_at: **Optional[datetime]**
    - user: **UserOut**
    """

    db_tweet = tweet_crud.get_tweet(db, tweet_id)
    
    if db_tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )
    
    tweet_crud.update_tweet(db, tweet_id, tweet)
    
    return db_tweet
    
    # if res.user_id != request_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You are not allowed to perfom this action"
    #     )
    
    
# Delete a tweet
@tweet.delete(
    path="/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Tweet"
)
def delete_tweet(
    tweet_id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID you want to delete",
        example=1
    ),
    db: Session = Depends(get_db)
):
    """
    Delete tweet
    
    This path operation deletes a specific tweet in the app.
    Only the tweet owner can update the tweet.
    
    Parameters:
    - Path parameters:
        - id: **int**
        
    Returns:
        -
    """
    
    db_tweet = tweet_crud.get_tweet(db, tweet_id)
    
    if db_tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )
    
    tweet_crud.delete_tweet(db, tweet_id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # if tweet_response.user_id != request_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail='You are not allowed to perform this action'
    #     )


