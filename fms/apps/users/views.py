import json
from flask import request,session, jsonify, make_response, Blueprint, abort, g, redirect
from flask.views import MethodView
from fms.apps.users import models
from fms.database import db_session
from sqlalchemy.sql.expression import literal_column
from fms import app
 
user_blueprint = Blueprint('user',__name__)
 
@user_blueprint.route('/users',methods=['GET'])
def load_user(id=None):
	id = request.args.get('id')
	res = {}
	if not id:
		users = models.User.query.all()
		for user in users:
			res[user.id] = {
				'username': user.username,
				'email': user.email,
				'password': user.password,				
			}
	else:
		user = db_session.query(models.User).filter(models.User.id==id).first()
		if not user:
			abort(404)
		res = {
			'username': user.username,
			'email': user.email,
			'password': user.password,			
		}	
	return jsonify(res)
	
@user_blueprint.route('/users',methods=['POST'])
def new_user():	
	# read the posted values from the UI
	_username = request.form['signupUsername']
	_password = request.form['signupPassword']
	_email = request.form['signupEmail']	
	
	# validate the received values
	if (_username and _password and _email):
		#user = models.User.query.get(_email)
		try:
			user = db_session.query(models.User).filter(models.User.username==_username).first()
			if not user:		
				user = models.User(username=_username, email=_email, password=_password, created_by='User Registered')
				db_session.add(user)
				db_session.commit()
				auth_token = models.User.encode_auth_token(user.id)
				responseObject = {
					'status': 'success',
					'message': 'Successfully registered.',
					'auth_token': auth_token
				}
				return make_response(jsonify(responseObject)), 201
			else:
				responseObject = {
					'status': 'fail',
					'message': 'Some error occurred. Please try again.'
				}
				return make_response(jsonify(responseObject)), 202
		except Exception as e:
			responseObject = {
				'status': 'fail',
				'message': 'Some error occurred. Please try again.'
			}
			return make_response(jsonify(responseObject)), 401		
	else:
		return jsonify({'error':'Missing data, user created unsuccessful !'})

@user_blueprint.route('/users/login',methods=['POST'])
def user_login():
	_username = request.form['loginUsername']
	_password = request.form['loginPassword']
	try:
		#user = models.User.query.filter(models.User.username == _username)
		#user = db_session.query(models.User).filter(models.User.username == _username)
		user = db_session.query(models.User).filter(models.User.username==_username).one()
		if user:
			if  models.User.password_is_valid(user,_password):
				session['user_id'] = user.id
				return redirect('/')
				#g.user = user
				#auth_token = models.User.encode_auth_token(user,user.id)
				#auth_token = '8a3971a57fea4db08d86aa844e8ecefe'
				#if auth_token:
				#	responseObject={
				#		'status': 'success',
				#		'message': 'Successfully logged in.',
				#		'auth_token': auth_token
				#	}
				#	return make_response(jsonify(responseObject)), 200
		else:
			responseObject={
				'status': 'unsuccess',
				'message': 'UnSuccessful user or password wrong!.'				
			}
			return make_response(jsonify(responseObject)), 200
	except Exception as e:
		print(e)
		responseObject={
			'status': 'fail',
			'message': 'Try again'
		}
		return make_response(jsonify(responseObject)), 500

@user_blueprint.route('/users/logout',methods=['GET'])
def user_logout():
	if session.get('user_id'):	
		session.pop('user_id',None)
		return redirect('/')