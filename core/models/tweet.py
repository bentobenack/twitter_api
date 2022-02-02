
#Python
from datetime import datetime

#SQLAlchemy
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import TIMESTAMP, ForeignKey, Table, Column

#PyMySQL
from pymysql import Date

#Settings
from settings.db import meta

#Tweet Table
tweets = Table(
    "tweets",
    meta,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("content", String(255), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("update_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)