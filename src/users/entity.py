from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


db_url = 'localhost:5432';
db_name = 'test'
db_user = 'postgres'
db_password = 'root'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Entity():
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	email = Column(String)
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	last_updated_by = Column(String)	
	
	def __init__(self, username, password, email,created_by):
		self.username = username
		self.password = password
		self.email = email
		self.created_at=datetime.now()
		self.updated_at=datetime.now()
		self.last_updated_by=created_by
		
		