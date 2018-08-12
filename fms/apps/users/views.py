import json
from flask import request, jsonify, Blueprint, abort, g
from flask.views import MethodView
from fms.apps.users import models
from fms.database import db_session
from fms import app
 
user_blueprint = Blueprint('user',__name__)
 
@user_blueprint.route('/users')
def user(id=None, page=1):
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
		user = models.User.query.get(id)
		if not user:
			abort(404)
		res = {
			'username': user.username,
			'email': user.email,
			'password': user.password,			
		}	
	return jsonify(res)
	
@user_blueprint.route('/users',methods=['POST'])
def addUser():	
	# read the posted values from the UI
	_username = request.form['signupUsername']
	_password = request.form['signupPassword']
	_email = request.form['signupEmail']	
	
    # validate the received values
	if (_username and _password and _email):
		user = models.User(username=_username, email=_email, password=_password, created_by='User Registered')
		db_session.add(user)
		db_session.commit()
		return jsonify({user.id: {
			'username': user.username,
			'email': user.email,
		}})

	else:
		return jsonify({'error':'Missing data, user created unsuccessful !'})