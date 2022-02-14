from os import getcwd, remove
import shutil
import secrets

from typing import List

from fastapi import APIRouter, Body, File, Path, UploadFile
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from api.v1.files.schemas.file import CreateFile, FileOut

from api.v1.users.schemas.user import User as UserSchema
from config.db_config import get_db
from api.v1.users.services import user as user_crud
from api.v1.files.services import file as file_crud
from api.v1.tweets.services import tweet as tweet_crud
from api.v1.auth.middlewares.auth import get_current_user



file = APIRouter()

# User

## Upload Image Profile
@file.post(
    path="/profile/img",
    status_code=status.HTTP_200_OK,
    summary="Upload a profile img",
    tags=["Files", "Users"],
    response_model=FileOut
)
def upload_profile_img(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    db_user = user_crud.get_user(db, request_user.id)
        
    if db_user.id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perfom this action"
        )
        
    path = getcwd() + "/src/api/v1/static_files/profile_imgs/"
    new_filename = secrets.token_hex(20) + "." + file.content_type.split("/")[1]
    
    try:
        with open(path + new_filename, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
    
    user_crud.update_user_specific_fild(db, request_user.id, "file_url", path+new_filename)
   
    return file_crud.create_file(db, CreateFile(
            file_url=path+new_filename, 
            user_id=request_user.id, 
            tweet_id=None
        ))
    
    

## Get a Profile Picture
@file.get(
    path="/profile/img",
    status_code=status.HTTP_200_OK,
    summary="Get a Profile Img",
    tags=["Files", "Users"]
)
def get_profile_img(
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    db_user = user_crud.get_user(db, request_user.id)
    
    if db_user.id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perfom this action"
        )
    
    if db_user.file_url is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Image not found"
        )
        
    return FileResponse(db_user.file_url)


## Delete a Profile Picture
@file.delete(
    path="/profile/img",
    status_code=status.HTTP_200_OK,
    summary="Delete a Profile Img",
    tags=["Files", "Users"]
)
def delete_profile_img(
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    db_user = user_crud.get_user(db, request_user.id)
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
        
    if db_user.id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perfom this action"
        )
        
    try:
        remove(db_user.file_url)
    except FileNotFoundError:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="File not Found"
        )
        
    if db_user.file_url is not None:
        file_crud.delete_file_by_url(db, db_user.file_url)
    
    user_crud.update_user_specific_fild(db, request_user.id, "file_url", None)
    
    
# Tweet

## Upload Tweet File
@file.post(
    path="/tweet/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Upload a Tweet File",
    tags=["Files", "Tweets"],
    response_model=List[FileOut]
)
def upload_tweet_file(
    tweet_id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID",
        example=1
    ),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    
    db_tweet = tweet_crud.get_tweet(db, tweet_id)
    
    if db_tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )
    
    if db_tweet.user_id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not allowed to perfom this action'
        )
        
    for file in files:
        
        path = getcwd() + "/src/api/v1/static_files/tweets/"
        new_filename = secrets.token_hex(20) + "." + file.content_type.split("/")[1]
        
        try:
            with open(path + new_filename, "wb") as f:
                shutil.copyfileobj(file.file, f)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong"
            )
   
        file_crud.create_file(db, CreateFile(file_url=path+new_filename, tweet_id=tweet_id, user_id=None))

    return file_crud.get_files_by_tweet(db, tweet_id)
    
    
## Get Tweet files
@file.get(
    path="/tweet/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Get Tweet Files",
    tags=["Files", "Tweets"],
    response_model=List[FileOut]
)
def get_tweet_files(
    tweet_id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID",
        example=1
    ),
    db: Session = Depends(get_db),
):
    db_tweet = tweet_crud.get_tweet(db, tweet_id)
        
    if db_tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )
    
    return file_crud.get_files_by_tweet(db, tweet_id)
    
    # for file in res:
    #     yield FileResponse(file.file_url)


## Delete a Tweet File
@file.delete(
    path="/tweet/{tweet_id}/{file_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet File",
    tags=["Files", "Tweets"]
)
def delete_profile_img(
    tweet_id: int = Path(
        ...,
        gt=0,
        title="Tweet ID",
        description="The tweet ID",
        example=1
    ),
    file_id: int = Path(
        ...,
        gt=0,
        title="File ID",
        description="The File ID",
        example=1
    ),
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    db_file = file_crud.get_file(db, file_id)
    db_tweet = tweet_crud.get_tweet(db, tweet_id)
    
    if db_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File Not Found"
        )
    
    if db_tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found"
        )   
        
    if db_tweet.user_id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perfom this action"
        )
        
    if db_tweet.id == db_file.tweet_id:
        try:
            remove(db_file.file_url)
        except FileNotFoundError:
            HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="File not Found"
        )
            
        file_crud.delete_file(db, file_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The file and the tweet dont match"
        )
        