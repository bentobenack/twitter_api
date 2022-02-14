
#Python
from datetime import datetime

#SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy import TIMESTAMP, ForeignKey, Column
from sqlalchemy.orm import relationship

#Settings
from config.db_config import Base

#Tweet Table
class Tweet(Base):
    __tablename__="tweets"
    
    id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=None, onupdate=datetime.utcnow)
    
    owner_user = relationship("User", back_populates="tweets")
    files = relationship("File", back_populates="owner_tweet")
