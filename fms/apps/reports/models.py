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
	content = Column(String(255))	
	reported_at = Column(DateTime())
	lat = Column(Float())
	lng = Column(Float())
	reported_at = Column(DateTime, default=datetime.now)
	user_report_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)	
	report_images = relationship("ReportImage", backref="reports",lazy='dynamic')
	
	# System fields
	is_active = Column(Boolean())
	is_delete = Column(Boolean())
	is_verified = Column(Boolean())
	edited_at = Column(DateTime, default=datetime.now)
	last_updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
	
	

class ReportImage(Base):
	__tablename__ = 'report_images'
	
	id = Column(Integer, primary_key=True)	
	image_path = Column(String(255))			
	report_id = Column(Integer, ForeignKey('reports.id', ondelete='CASCADE'), nullable=False)	
	
	geom = Column(Geometry(geometry_type='POINT', srid=4326))	
	uploaded_at = Column(DateTime, default=datetime.now)	
	
	# System fields
	is_active = Column(Boolean())
	is_delete = Column(Boolean())
	is_verified = Column(Boolean())
	edited_at = Column(DateTime, default=datetime.now)
	
	
	