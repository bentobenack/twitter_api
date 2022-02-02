from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://bentobenack:bentobenack@localhost:3306/")

meta = MetaData()

conn = engine.connect()