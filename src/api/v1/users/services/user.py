
from sqlalchemy.orm import Session
from api.v1.auth.utils.password import hash_password

from api.v1.users.models.user import User
from api.v1.users.schemas.user import CreateUser

from cryptography.fernet import Fernet


# Password encription configuration
key = Fernet.generate_key()
fernet = Fernet(key)

# Create a user
def create_user(db: Session, user: CreateUser):
    
    new_user = user.dict()
    new_user["password"] = hash_password(new_user['password'])
    
    db_user = User(**new_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
    

# Get a User
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Get Users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


# Update a user
def update_user(db: Session, user_id: int, user: CreateUser):
    
    updated_user = {**user.dict()}
    
    updated_user["password"] = fernet.encrypt(user.password.encode("utf-8"))
    
    db.query(User).filter(User.id == user_id).update({**updated_user})
    db.commit()
    
    return get_user(db, user_id)


# Delete a User
def delete_user(db: Session, user_id: int):
    res = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    
    
    