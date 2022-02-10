# FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from config.db_config import get_db
from api.v1.users.services import user as user_crud

# Schemas
from api.v1.users.schemas.user import CreateUser
from api.v1.users.schemas.user import UserOut
from api.v1.auth.schemas.auth import LoginRequest
from api.v1.auth.schemas.auth import LoginReponse
from api.v1.auth.schemas.auth import BaseJWTRefreshToken
from api.v1.auth.schemas.auth import JWTAccessToken

# Utils
from api.v1.auth.utils.password import check_password
from api.v1.auth.utils.jwt import create_credentials
from api.v1.auth.utils.jwt import create_access_token
from api.v1.auth.utils.jwt import verify_token


auth = APIRouter()


@auth.post(
    path='/signup',
    response_model=LoginReponse,
    status_code=status.HTTP_201_CREATED,
    summary='Sign up',
    tags=['Auth', 'Users']
)
def signup(user: CreateUser = Body(...), db: Session = Depends(get_db)):
    """
    Sign up
    
    This path operation registers a new user in the app.
    
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
    new_user = user_crud.create_user(db, user)
    
    response = {
        'user': new_user,
    }
    response.update(create_credentials(response['user']))

    return response


@auth.post(
    path='/login',
    response_model=LoginReponse,
    status_code=status.HTTP_200_OK,
    summary='Login',
    tags=['Auth', 'Users']
)
def login(user: LoginRequest = Body(...), db: Session = Depends(get_db)):
    """
    Login
    
    This operation path allows a user to login in the app.
    
    Parameters:
    - Request body parameters:
        - user: **LoginRequest**
        
    Returns a json object with the information of the logged user.
    - user: **UserOut**
    - access_token: **str**
    - access_token_expiration: **int**
    - refresh_token: **str**
    - refresh_token_expiration: **int**
    """

    db_user = user_crud.get_user_by_email(db, user.email)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    password_match = check_password(user.password, db_user.password)

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    response = {
        'user': UserOut(
            birth_date=db_user.birth_date,
            created_at=db_user.created_at,
            email=db_user.email,
            first_name=db_user.first_name,
            id=db_user.id,
            last_name=db_user.last_name,
            updated_at=db_user.updated_at
        ),
    }
    response.update(create_credentials(response['user']))

    return response


@auth.post(
    path='/refresh',
    response_model=JWTAccessToken,
    status_code=status.HTTP_200_OK,
    summary='Refresh token',
    tags=['Auth', 'Users']
)
def refresh_token(refresh_token: BaseJWTRefreshToken = Body(...), db: Session = Depends(get_db)):
    """
    Refresh token
    
    This operation path allows a user to refresh the access token.
    
    Parameters:
    - Request body parameters:
        - refresh_token: **BaseJWTRefreshToken**
        
    Returns a json object with the new access token information.
    - access_token: **str**
    - access_token_expiration: **int**
    """

    decoded_token = verify_token(refresh_token.refresh_token)

    base_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid token'
    )

    if decoded_token is None:
        raise base_exception
    
    db_user = user_crud.get_user(db, decoded_token['sub'])

    if db_user is None:
        raise base_exception

    token, expiration = create_access_token({
        'sub': db_user.id,
        'email': db_user.email,
        'name': db_user.first_name + " " + db_user.last_name,
    })

    response = {
        'access_token': token,
        'access_token_expiration': expiration,
    }

    return response