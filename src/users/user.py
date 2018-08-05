from sqlalchemy import Column, String
from .entity import Entity, Base
from marshmallow import Schema, fields

class User(Entity, Base):
	__tablename__= 'users'
	
	username = Column(String)
	password = Column(String)
	email = Column(String)
	
	def __init__(self, username, password, email, created_by):
		Entity.__init__(self,created_by)
		self.username = title
		self.password = password
		self.email = email
		
class UserSchema(Schema):
	id = fields.Number()
	username = fields.Str()
	password = fields.Str()
	email = fields.Str()
	created_at = fields.DateTime()
	updated_at = fields.DateTime()
	last_updated_by = fields.Str()