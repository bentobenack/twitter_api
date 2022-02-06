
#Python
from datetime import datetime

#SQLAlchemy
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import TIMESTAMP, ForeignKey, Table, Column

#Settings
from core.config.db import meta, engine

#Tweet Table
Tweets = Table(
    "tweets",
    meta,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("content", String(255), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=None, onupdate=datetime.utcnow)
)

#Create/Generate the table in database
meta.create_all(engine)