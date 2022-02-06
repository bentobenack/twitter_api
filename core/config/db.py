from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://bentobenack:bentobenack@localhost:3306/twitterdb")

meta = MetaData()

connection = engine.connect()