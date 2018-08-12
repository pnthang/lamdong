from fms.database import Base
from sqlalchemy import Column, Integer, String, DateTime,Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.postgresql import JSON
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	
	# User authentication information
	username = Column(String(30))
	password = Column(String(255))
	
	# User email information
	email = Column(String(50))
	confirmed_at = Column(DateTime())
	
	# User information
	first_name = Column(String(30))
	last_name = Column(String(30))
	is_active = Column(Boolean())
	is_delete = Column(Boolean())
	is_verified = Column(Boolean())
	created_at = Column(DateTime, default=datetime.now)
	edited_at = Column(DateTime, default=datetime.now)
	last_updated_by = Column(String(50))		
	
	groups = association_proxy('_user_group_roles', 'groups')
	roles = association_proxy('_user_group_roles', 'roles')
	
	def __init__(self, username, password, email,created_by):
		self.username = username
		self.password = Bcrypt().generate_password_hash(password).decode()
		self.email = email
		created_at = datetime.now
		edited_at = datetime.now	
		self.last_updated_by=created_by
		
	def password_is_valid(self, password):
		return Bcrypt().check_password_hash(self.password, password)
		
	def __repr__(self):
		return "User[email=%s, name=%s, first_name=%s, last_name=%s]" % (self.username, self.email, self.password, self.last_updated_by)

class Role(Base):
	__tablename__ = 'roles'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(30), unique=True)
	description = Column(String)
	
	def __init__(self, name, description):
		self.name = name
		self.description = description		
		
	def __repr__(self):
		return self.name

class Group(Base):
	__tablename__ = 'groups'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(30), unique=True)
	description = Column(String)
	
	users = association_proxy('_user_group_roles', 'users')

	def __init__(self, name, description):
		self.name = name
		self.description = description
	
	def __str__(self):
		return self.name

class UserGroupRole(Base):
	__tablename__ = 'user_group_roles'
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
	group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
	role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
	
	group = relationship(Group, backref=backref('_user_group_roles', cascade='all, delete-orphan'))
	role = relationship(Role)
	user = relationship(User, backref=backref('_user_group_roles', cascade='all, delete-orphan'))