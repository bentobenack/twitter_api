from fastapi import HTTPException, status
import jwt

from typing import Tuple
from typing import Union
from typing import Any
from typing import Dict
from datetime import datetime
from datetime import timedelta

from config import settings
from api.v1.users.schemas.user import UserOut


def create_access_token(data: dict) -> Tuple[str, float]:
    """
    Create a JWT access token.
    Args:
        data (dict): The data to encode in the token.
    Returns:
        Tuple[str, int]: The access token and its expiration time.
    """

    payload = data.copy()

    
    expiration_time = (datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION))

    payload['type'] = settings.JWT_ACCESS_TOKEN_TYPE
    payload['exp'] = expiration_time.timestamp()
    payload['iat'] = (expiration_time - timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION)).timestamp()
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token, payload['exp'], payload['iat']


def create_refresh_token(data: dict) -> Tuple[str, float]:
    """
    Create a JWT refresh token.
    Args:
        data (dict): The data to encode in the token.
    Returns:
        Tuple[str, int]: The refresh token and its expiration time.
    """

    payload = data.copy()

    
    expiration_time = (datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRATION))

    payload['type'] = settings.JWT_REFRESH_TOKEN_TYPE
    payload['exp'] = expiration_time.timestamp()
    payload['iat'] = (expiration_time - timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRATION)).timestamp()

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token, payload['exp'], payload['iat']


def create_credentials(user: Union[dict, UserOut]) -> Dict[str, Any]:
    """
    Create the credentials for a user.
    Args:
        user (Union[dict, User]): The user to create the credentials for.
    Returns:
        Tuple[str, str]: The access token and the refresh token.
    """

    if isinstance(user, dict):
        user_payload = {
            'sub': user['id'],
            'email': user['email'],
            'name': f"{user['first_name']} {user['last_name']}",
        }
    else:
        user_payload = {
            'sub': user.id,
            'email': user.email,
            'name': user.first_name + " " + user.last_name,
        }

    access_token, access_expiration_time, access_created_time = create_access_token(user_payload)
    refresh_token, refresh_expiration_time, refresh_created_time = create_refresh_token({
        'sub': user_payload['sub'],
    })

    output = {
        'access_token': access_token,
        'access_token_expiration': access_expiration_time - access_created_time,
        'refresh_token': refresh_token,
        'refresh_token_expiration': refresh_expiration_time - refresh_created_time
    }

    return output


def verify_token(token: str) -> Union[Dict[str, Any], None]:
    """
    Verify a JWT token.
    Args:
        token (str): The token to verify.
    Returns:
        Union[Dict[str, Any], None]: The decoded token if valid, None otherwise.
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.exceptions.InvalidSignatureError:
        return None
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None

    if payload["exp"] < datetime.utcnow().timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return payload