import json
import os
from flask import request,session, jsonify, make_response, Blueprint, abort, g, redirect, url_for 
from fms.apps.reports import models
from fms.database import db_session
from sqlalchemy import func
from sqlalchemy.sql.expression import literal_column
from fms import app
from werkzeug import secure_filename
from fms.apps.utilities.images import *
from thumbnails import get_thumbnail

report_blueprint = Blueprint('report',__name__)

_upload_folder = app.config['UPLOAD_FOLDER']
_allowed_extensions = app.config['ALLOWED_EXTENSIONS']
_server_name = app.config['SERVER_NAME']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in _allowed_extensions
		   
@report_blueprint.route('/reports',methods=['GET'])
def load_report(id=None):
	id = request.args.get('id')
	res = []  
	if not id:
		reports = db_session.query(models.Report)		
		for report in reports:
			images=[]
			report_images= db_session.query(models.ReportImage).filter(models.ReportImage.report_id==report.id)			
			for report_image in report_images:
				i = {
					'l_image_path':report_image.l_image_path,
					'm_image_path':report_image.m_image_path,
					's_image_path':report_image.s_image_path
				}
				images.append(i)  
			r = {
				"type": "Feature",
				"geometry": {
					"type": "Point",
					"coordinates": [report.lng, report.lat]
				},
				"properties": {
					'content': report.content,
					'reported_at': report.reported_at,
					'images':images
				}
			}
			res.append(r)  
	else:
		report = db_session.query(models.Report).filter(models.Report.id==id).first()		
		if not report:
			abort(404)			
		report_images= db_session.query(models.ReportImage).filter(models.ReportImage.report_id==report.id)
		images=[]
		for report_image in report_images:
			images[report_image.id] = {
				'l_image_path':report_image.l_image_path,
				'm_image_path':report_image.m_image_path,
				's_image_path':report_image.s_image_path
			}
			images.append(i)
		res = {
			'content': report.content,
			'reported_at': report.reported_at,				
			'location': {
				'lat': report.lat,
				'long':report.lng,
			},
			'images':images
		}
	return jsonify(res)
	
@report_blueprint.route('/reports',methods=['POST'])
def new_report():
	if not session.get('user_id'):
		return redirect('/')
	else:		
		# read the posted values from the UI		
		_content = request.form['reportContent']		
		_lat = str(request.form['reportLat'])
		if not _lat:
			_lat=12.0113			
		_lng = str(request.form['reporLng'])
		if not _lng:
			_lng=108.4194
		_user_report_id = str(session.get('user_id'))		
		_last_updated_by = str(session.get('user_id'))		
		
		_image_path ='/#'
		error_message =''
		report_images=[]
		# check if the post request has the file part
		if 'reportImage' not in request.files:
			error_message = 'No file part'	
		files = request.files.getlist('reportImage[]')
		for file in files:
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				error_message = 'No selected file'
			if file and allowed_file(file.filename):
				# Make the filename safe, remove unsupported chars
				filename = secure_filename(file.filename)
				filename = filename.lower()
				max_report_id = db_session.query(func.max(models.Report.id)).scalar()
				if not max_report_id:
					max_report_id = 1
				else:
					max_report_id= int(max_report_id) + 1
				location = "rp" + str(max_report_id)
				path = os.path.join('fms',_upload_folder, str(session.get('user_id')),location)				
				if not os.path.exists(path):
					os.makedirs(path)
								
				file.save(os.path.join(path,filename))
				#_image_path = url_for('static',filename=filename)				
				_image_path=os.path.join(_upload_folder, str(session.get('user_id')),location,filename)
				_image_path = _image_path.replace('\\','/')
				
				image = Image.open(os.path.join(path,filename))
				_image_metadata = get_exif_data(image)
				_latlng = get_lat_lon(_image_metadata)
				
				image.thumbnail((1024, 768), Image.ANTIALIAS)
				image.save(os.path.join(path,"l_" + filename), "JPEG")
				_l_image=os.path.join(_upload_folder, str(session.get('user_id')),location,"l_"+ filename)
				_l_image=_l_image.replace('\\','/')
				
				image.thumbnail((320, 240), Image.ANTIALIAS)
				image.save(os.path.join(path,"m_" + filename), "JPEG")
				_m_image=os.path.join(_upload_folder, str(session.get('user_id')),location,"m_"+ filename)
				_m_image = _m_image.replace('\\','/')			
				
				image.thumbnail((160, 120), Image.ANTIALIAS)
				image.save(os.path.join(path,"s_" + filename), "JPEG")
				_s_image=os.path.join(_upload_folder, str(session.get('user_id')),location,"s_"+ filename)
				_s_image=_s_image.replace('\\','/')
				
				_geom = 'SRID=4326;POINT(%s %s)' % (_latlng[1],_latlng[0])	
				# default current lat lng of device					
				if not _latlng[0]:
					_geom = 'SRID=4326;POINT(%s %s)' % (_lng,_lat)
				_report_geom = 'SRID=4326;POINT(%s %s)' % (_lng,_lat)
				report_images.append(models.ReportImage(image_path=_image_path,l_image_path=_l_image,m_image_path=_m_image,s_image_path=_s_image,geom=_geom))				
				
		if (_content):				
			try:
				report = models.Report(content=_content,lat=_lat,lng=_lng,user_report_id=_user_report_id,last_updated_by=_last_updated_by,geom=_report_geom)
				db_session.add(report)
				for report_image in report_images:
					report.report_images.append(report_image)
					db_session.add(report_image)
				db_session.commit()				
				responseObject = {
					'status': 'success',
					'message': 'Successfully reported.',					
				}
				return make_response(jsonify(responseObject)), 201
			except Exception as e:
				responseObject = {
					'status': 'fail',
					'message': 'Some error occurred. Please try again.',
					'code': str(e)
				}
				return make_response(jsonify(responseObject)), 401		
		else:
			return jsonify({'error':'Missing data, user created unsuccessful !'})