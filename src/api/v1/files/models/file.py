
#Python
from datetime import datetime

#SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import TIMESTAMP, ForeignKey, Column
from sqlalchemy.orm import relationship

#Settings
from config.db_config import Base

#File Table
class File(Base):
    __tablename__="files"
    
    id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    file_url = Column(String(255), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, default=None)
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True, default=None)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=None, onupdate=datetime.utcnow)
    
    owner_user = relationship("User", back_populates="files")
    owner_tweet = relationship("Tweet", back_populates="files")