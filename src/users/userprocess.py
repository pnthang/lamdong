from flask import Blueprint
from flask import Flask, abort, request, jsonify
import json
from flask import jsonify
from .entity import Session, engine, Base
from .user import User, UserSchema

mod = Blueprint('User',__name__)

Base.metadata.create_all(engine)

@mod.route('/users')
def get_exams():
	session = Session()
	user_objects = session.query(User).all()
	
	schema = UserSchema(many=True)
	users = schema.dump(user_objects)
	
	session.close()
	return jsonify(users.data)
	
@mod.route('/users',methods=['POST'])
def add_exam():
	posted_user = UserSchema(only=('username','password','email')).load(request.get_json())
	
	user = User(**posted_user.data, created_by="HTTP post request")
	
	session = Session()
	session.add(user)
	session.commit()
	
	new_user = UserSchema().dump(user).data
	session.close()
	return jsonify(new_user), 201
	
session = Session()
exams = session.query(Exam).all()

@mod.route('/user/add',methods=['POST'])
def addfilm():	
	#return request
	#if not request.get_json(force=True):
	#	abort(400)	
	# read the posted values from the UI
	_signupUsername = request.form['signupUsername']
	_signupEmail = request.form['signupEmail']
	_signupPassword = request.form['signupPassword']
	
    # validate the received values
	if (_signupUsername and _signupEmail and _signupPassword):
		clsUser = clsUser()
		clsUser.addNewUser(signupUsername,signupEmail,signupPassword)
		return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
	
			

@mod.route('/user/get',methods=['GET'])
def getFilms():  
    films = []
    clsUser = clsUser()
    filmData = clsUser.getUsers()  
    for r in filmData:    
        a = {"signupUsername": r[0], "signupEmail": r[1], "signupPassword":r[2]}  
        films.append(a)  
      
    return jsonify(films)

@mod.route('/user/createUserTable')  
def createUserTable():
    clsUser = clsUser()  
    clsUser.createTable();  
    result = {"result": "Users Table Created"}
    return jsonify(result) 

	
class JSONObject:  
  def __init__( self, dict ):  
      vars(self).update( dict ) 