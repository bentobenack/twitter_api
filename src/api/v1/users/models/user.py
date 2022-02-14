
#Python
from datetime import datetime

#SQLAlchemy
from sqlalchemy import Integer, String, Date, TIMESTAMP, Boolean
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from ...tweets.models.tweet import Tweet

#Settings
from config.db_config import Base

#User Table
class User(Base):
    __tablename__="users"
    
    id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)
    img_url = Column(String(255), unique=True, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=None, onupdate=datetime.utcnow)
    
    tweets = relationship("Tweet", back_populates="owner")
    
