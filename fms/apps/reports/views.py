import json
import os
from flask import request,session, jsonify, make_response, Blueprint, abort, g, redirect, url_for 
from fms.apps.reports import models
from fms.database import db_session
from sqlalchemy.sql.expression import literal_column
from fms import app
from werkzeug import secure_filename
from fms.apps.utilities.images import *

report_blueprint = Blueprint('report',__name__)

_upload_folder = app.config['UPLOAD_FOLDER']
_allowed_extensions = app.config['ALLOWED_EXTENSIONS']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in _allowed_extensions
		   
@report_blueprint.route('/reports')
def load_report(id=None):
	res = {}
	if not id:
		reports = models.Report.query.all()
		for report in reports:
			res[report.id] = {
				'content': report.content,
				'reported_at': report.reported_at,
				'image_path': report.image_path,
				'location': {
					'lat': report.lat,
					'long':report.long,
				}
			}
	else:
		report = models.Report.query.get(id)
		if not report:
			abort(404)
		res[report.id] = {
			'content': report.content,
			'reported_at': report.reported_at,
			'image_path': report.image_path,
			'location': {
				'lat': report.lat,
				'long':report.long,
			}
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
		_lng = str(request.form['reporLng'])
		_user_report_id = str(session.get('user_id'))		
		_last_updated_by = str(session.get('user_id'))
		
		_image_path ='/#'
		error_message =''
		# check if the post request has the file part
		if 'reportImage' not in request.files:
			error_message = 'No file part'	
		file = request.files['reportImage']
        # if user does not select file, browser also
        # submit a empty part without filename
		if file.filename == '':
			error_message = 'No selected file'
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(_upload_folder,filename))
			_image_path = url_for('report.new_report',filename=filename)
			#_image_path = os.path.join(_upload_folder,filename)
			image = Image.open(os.path.join(_upload_folder,filename))
			exif_data = get_exif_data(image)
			_latlng = get_lat_lon(exif_data)
			_img_lat =_latlng[0]
			_img_lng =_latlng[1]
		# validate the received values
		if (_content):				
			try:
				report = models.Report(content=_content,image_path=_image_path,lat=_lat,lng=_lng,user_report_id=_user_report_id,last_updated_by=_last_updated_by,img_lat=_img_lat,img_lng=_img_lng)
				db_session.add(report)
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