
#Python
from datetime import datetime

#SQLAlchemy
from sqlalchemy.sql.sqltypes import Integer, String, Date, TIMESTAMP
from sqlalchemy import Table, Column

#Settings
from core.config.db import meta, engine

#User Table
users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(50), nullable=False),
    Column("birth_date", Date, nullable=True),
    Column("email", String(120), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("update_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

#Create/Generate the table in database
meta.create_all(engine)