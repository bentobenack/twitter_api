
from sqlalchemy.orm import Session

from api.v1.files.models.file import File
from api.v1.files.schemas.file import CreateFile

# Create a file
def create_file(db: Session, file: CreateFile):
    
    db_file = File(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return db_file
    

# Get a file
def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()


# Get a file by url
def get_file_by_url(db: Session, file_url: str):
    return db.query(File).filter(File.file_url == file_url).first()


# Get Files
def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(File).offset(skip).limit(limit).all()


# Update a file
def update_file(db: Session, file_id: int, file: CreateFile):
    
    db.query(File).filter(File.id == file_id).update(values={**file.dict()})
    db.commit()
    
    
# Update a file in specific field
def update_file_specific_fild(db: Session, file_url: str, field: str, content):
    
    db.query(File).filter(File.file_url == file_url).update({field: content})
    db.commit()
    
    return get_file_by_url(db, file_url)


# Get Files by Tweet
def get_files_by_tweet(db: Session, tweet_id: int):
    return db.query(File).filter(File.tweet_id == tweet_id).all()
    

# Get file by user
def get_file_by_user(db: Session, user_id: int):
    return db.query(File).filter(File.id == user_id).first()


# Delete a File by url
def delete_file_by_url(db: Session, file_url: str):
    db.query(File).filter(File.file_url == file_url).delete()
    db.commit()
    
# Delete a File by url
def delete_file(db: Session, file_id: int):
    db.query(File).filter(File.id == file_id).delete()
    db.commit()
    
    


    
    
    