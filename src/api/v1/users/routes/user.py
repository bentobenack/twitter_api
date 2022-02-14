
from typing import List, Optional

from fastapi import APIRouter, Body, File, Path, Query, Response, UploadFile
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.orm import Session

from cryptography.fernet import Fernet

from api.v1.users.schemas.user import CreateUser, UserOut, User as UserSchema
from config.db_config import get_db
from api.v1.users.services import user as user_crud
from api.v1.auth.middlewares.auth import get_current_user

from os import getcwd

user = APIRouter()

# Password encription configuration
key = Fernet.generate_key()
fernet = Fernet(key)

#Get current User
@user.get(
    path="/me",
    tags=["Users"],
    summary="Get Me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK
)
def get_me(
    request_user: UserSchema = Depends(get_current_user),
):
    return request_user


# Read All Users
@user.get(
    path="/",
    tags=["Users"],
    summary="Get Users",
    response_model=List[UserOut],
    status_code=status.HTTP_200_OK,
    
)
def get_users(
    skip: Optional[int] = Query(default=0),
    limit: Optional[int] = Query(default=100),
    db: Session = Depends(get_db)
):
    """
    Get Users
    
    This path operation shows all users.
    
    Parameters:
        - 
        
    Returns a list of json object with the information of all users.
    - id: **int**
    - first_name: **str**
    - last_name: **str**
    - email: **EmailStr**
    - created_at: **datetime**
    - updated_at: **datetime**
    """
    
    users = user_crud.get_users(db=db, skip=skip, limit=limit)
   
    return users


# Read a user
@user.get(
    path="/{user_id}",
    tags=["Users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    summary="Get a User"
)
def get_user(
    user_id: int = Path(
        ...,
        gt=0,
        title="User ID",
        description="The user ID you want to get",
        example=1
    ),
    db: Session = Depends(get_db)
):
    """
    Get user
        
    This path operation allows to get the information of a specific user.
    
    Parameters:
    - Path parameters:
        - id: **int**
        
    Returns a json object with the information of the user.
    - id: **int**
    - first_name: **str**
    - last_name: **str**
    - email: **EmailStr**
    - created_at: **datetime**
    - updated_at: **datetime**
    """
    
    db_user = user_crud.get_user(db, user_id)
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
        
    return db_user


# Update a user
@user.put(
    path="/{user_id}",
    tags=["Users"],
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    response_model=UserOut
)
def update_user(
    user_id: int = Path(
        ...,
        gt=0,
        title="User ID",
        description="The user ID you want to update",
        example=1
    ),
    user: CreateUser = Body(...),
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    """
    Update user.
    
    This operation path operation updates the information of a specific user.
    Users can only update their own information.
    
    Parameters:
    - Path parameters:
        - id: **int**
    - Body parameters:
        - user: **CreateUser**
        
    Returns the information of the updated user.
    - id: **int**
    - first_name: **str**
    - last_name: **str**
    - email: **EmailStr**
    - created_at: **datetime**
    - updated_at: **datetime**
    """
    
    db_user = user_crud.get_user_by_email(db, user.email)
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
        
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email alredy registered"
        )
     
    if db_user.id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perfom this action"
        )   
    
    return user_crud.update_user(db, user_id, user)
    
    
    
# Delete a user
@user.delete(
    path="/{user_id}",
    tags=["Users"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a User"
)
def delete_user(
    user_id: int = Path(
        ...,
        gt=0,
        title="User ID",
        description="The user ID you want to delete",
        example=1
    ),
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    """
    Delete user
    
    This path operation deletes a specific user.
    Users can only delete their own information.
    
    Parameters:
    - Path parameters:
        - id: **int**
        
    Returns:
        -
    """
    
    db_user = user_crud.get_user(db, user_id)
    
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
        
    user_crud.delete_user(db, user_id)
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
# Upload Image Profile
@user.post(
    path="/upload/img",
    status_code=status.HTTP_200_OK,
    summary="Upload Image Profile",
    tags=["Users"]
)
def upload_img_profile(
    img: UploadFile = File(...),
    db: Session = Depends(get_db),
    request_user: UserSchema = Depends(get_current_user),
):
    pass



