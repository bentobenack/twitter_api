
from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query, Response
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.orm import Session

from cryptography.fernet import Fernet

from core.schemas.user import CreateUser, UserOut
from core.config.dependency import get_db
from core.crud import user as user_crud



user = APIRouter()

# Password encription configuration
key = Fernet.generate_key()
fernet = Fernet(key)

#Create a user
@user.post(
    path="/users",
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    response_model=UserOut,
    summary="Create a user"
)
def create_user(user: CreateUser = Body(...), db: Session = Depends(get_db)):
    """
    Create a User
    
    This path operation registers a new user.
    
    Parameters:
    - Request body parameters:
        - user: **UserRegister**
        
    Returns a json object with the information of the registered user and its credentials.
    - user: **UserOut**
    - access_token: **str**
    - access_token_expiration: **int**
    - refresh_token: **str**
    - refresh_token_expiration: **int**
    """
    db_user = user_crud.get_user_by_email(db, user.email)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email alredy registered"
        )
        
    # res = connection.execute(Users.select().where(Users.columns.email == new_user["email"])).fetchone()
    
    return user_crud.create_user(db, user)
    
    

# Read All Users
@user.get(
    path="/users",
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
    path="/users/{user_id}",
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
    path="/users/{user_id}",
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
    db: Session = Depends(get_db)
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
    
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email alredy registered"
        )
    
    return user_crud.update_user(db, user_id, user)
    
    # if res.id != request_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You are not allowed to perfom this action"
    #     )
    
    
# Delete a user
@user.delete(
    path="/users/{user_id}",
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
    db: Session = Depends(get_db)
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
        
    user_crud.delete_user(db, user_id)
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    # if user_response.id != request_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail='You are not allowed to perform this action'
    #     )
    