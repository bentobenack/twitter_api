
import datetime
from typing import List
import pydottie

from fastapi import APIRouter, Body, Path, Response
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import text

from core.models.tweet import Tweets

from core.config.db import connection
from core.schemas.tweet import CreateTweet, TweetOut, BaseTweet, TweetWithRelations



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
    tweet: CreateTweet = Body(...)
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
    
    # Create tweet
    new_tweet = tweet.dict()
    
    res = connection.execute(Tweets.insert().values(**new_tweet))
    
    if res is None or (res.rowcount == 0):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!"
        )
    
    new_tweet["id"] = res.lastrowid
    new_tweet["created_at"] = datetime.datetime.utcnow()
    new_tweet["updated_at"] = None
    
    return new_tweet


# Get All Tweets
@tweet.get(
    path="/",
    tags=["Tweets"],
    summary="Get all Tweets",
    response_model=List[TweetWithRelations],
    status_code=status.HTTP_200_OK,
    
)
def get_all_Tweets():
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
    
    query = """
    SELECT
        t.id as 'id',
        t.content as 'content',
        t.created_at as 'created_at',
        t.updated_at as 'updated_at',
        u.id as 'user.id',
        u.first_name as 'user.first_name',
        u.last_name as 'user.last_name',
        u.birth_date as 'user.birth_date',
        u.email as 'user.email',
        u.created_at as 'user.created_at',
        u.updated_at as 'user.updated_at'
    FROM
        tweets as t
    INNER JOIN
        users as u
    ON
        t.user_id = u.id;
    """
    res = connection.execute(text(query)).fetchall()
    
    output = []
    
    for record in res:
        output.append(pydottie.transform(record))
   
    return output


# Get a tweet
@tweet.get(
    path="/{id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    response_model=TweetWithRelations,
    summary="Get a Tweet"
)
def get_tweet(
    id: int = Path(
        ...,
        gt=0,
        title=" ID",
        description="The tweet ID you want to get",
        example=1
    )
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
    
    
    query = """
    SELECT
        t.id as 'id',
        t.content as 'content',
        t.created_at as 'created_at',
        t.updated_at as 'updated_at',
        u.id as 'user.id',
        u.first_name as 'user.first_name',
        u.last_name as 'user.last_name',
        u.birth_date as 'user.birth_date',
        u.email as 'user.email',
        u.created_at as 'user.created_at',
        u.updated_at as 'user.updated_at'
    FROM
        tweets as t
    INNER JOIN
        users as u
    ON
        t.user_id = u.id
    WHERE
        t.id = :id;
    """
    
    res = connection.execute(text(query), id=id).fetchone()
    
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )
        
    return pydottie.transform(res)


# Update a tweet
@tweet.put(
    path="/{id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    response_model=TweetOut
)
def update_tweet(
    id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID you want to update",
        example=1
    ),
    tweet: BaseTweet = Body(...)
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
    res = connection.execute(Tweets.select().where(Tweets.c.id == id)).fetchone()
    
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )
    
    # if res.user_id != request_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You are not allowed to perfom this action"
    #     )
    
    
    # Update tweet
    connection.execute(Tweets.update(Tweets.c.id == id).values(**tweet.dict()))

    updated_tweet = {**res}    
    updated_tweet['updated_at'] = str(datetime.datetime.utcnow())
    
    return updated_tweet
    
    
# Delete a tweet
@tweet.delete(
    path="//{id}",
    tags=["Tweets"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Tweet"
)
def delete_tweet(
    id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID you want to delete",
        example=1
    )
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
    
    tweet_response = connection.execute(Tweets.select().where(Tweets.c.id == id)).fetchone()
    
    if tweet_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tweet not found'
        )
        
    # if tweet_response.user_id != request_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail='You are not allowed to perform this action'
    #     )
        
    # Delete tweet     
    connection.execute(Tweets.delete().where(Tweets.c.id == id))
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


