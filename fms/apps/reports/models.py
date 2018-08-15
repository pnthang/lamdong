from fms.database import Base
from sqlalchemy import Column, Integer, String, DateTime,Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from fms import app
from sqlalchemy.dialects.postgresql import JSON
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from geoalchemy2 import Geometry


class Report(Base):
	__tablename__ = 'reports'
	
	id = Column(Integer, primary_key=True)
	content = Column(String(30))
	image_path = Column(String(255))		
	reported_at = Column(DateTime())
	lat = Column(Float())
	lng = Column(Float())
	reported_at = Column(DateTime, default=datetime.now)
	user_report_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
	img_lat=Column(Float())
	img_lng=Column(Float())	
	
	# System fields
	is_active = Column(Boolean())
	is_delete = Column(Boolean())
	is_verified = Column(Boolean())
	edited_at = Column(DateTime, default=datetime.now)
	last_updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
	
	def __init__(self, content,image_path,lat,lng,user_report_id,last_updated_by,img_lat=None,img_lng=None):
		self.content = content	
		self.image_path=image_path
		self.lat=lat
		self.lng=lng
		self.img_lat=lat
		self.img_lng=lng
		#self.geom=geom
		self.user_report_id=user_report_id
		self.last_updated_by=last_updated_by
		#self.edited_at = datetime.now
		#self.created_at = datetime.now
		
	def __repr__(self):
		return "Report[content=%s]" % (self.content)