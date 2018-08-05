import json
from flask import Blueprint,Flask, abort, request, jsonify
from sqlalchemy import create_engine
from werkzeug import generate_password_hash, check_password_hash


POSTGRES_URL="127.0.0.1:5432"
POSTGRES_USER="postgres"
POSTGRES_PW="root"
POSTGRES_DB="test"
	
db_string ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

User = Blueprint('User',__name__)

@User.route('/user/signup',methods=['POST'])
def addUser():	
	# read the posted values from the UI
	_username = request.form['signupUsername']
	_password = request.form['signupPassword']
	_email = request.form['signupEmail']	
	
    # validate the received values
	if (_username and _password and _email):
		result = loadUser(_username)
		if (result):
			return json.dumps({'message':'User existed!'})
		else:
			_password = generate_password_hash(_password)
			result = addNew(_username,_password,_email)
			return json.dumps({'message':'User created successfully !' })
	else:
		return json.dumps({'error':'Missing data, user created unsuccessful !'})
	
@User.route('/user/login',methods=['POST'])
def loginUser():	
	# read the posted values from the UI
	_username = request.form['loginUsername']
	_password = request.form['loginPassword']		
	
    # validate the received values
	if (_username and _password):
		_password = generate_password_hash(_password)		
		result = loadUser(_username)
		if (_password == result):
			return json.dumps({'message':'User login successfully !'})
		else:
			return json.dumps({'error':'User login unsuccessful !'})

	#if not request.get_json(force=True):
	#	abort(400)			

@User.route('/users',methods=['GET'])
def getUsers():
	users = []
	list = getList()
	for r in list:
		a = {"username": r[0], "password": r[1], "email":r[2]}
		users.append(a)
	return jsonify(users) 


def addNew(username,password,email):
	db = create_engine(db_string)
	strSQL = "INSERT INTO users(username, password, email) VALUES ('"+username+"','"+password+"', '"+email+"')"
	result = db.execute(strSQL)
	return result

def getList():  
	db = create_engine(db_string)
	strSQL = "SELECT * FROM users"
	list = db.execute(strSQL)
	return list

def loadUser(username):  
	db = create_engine(db_string)
	strSQL = "SELECT password FROM users where username='" + username + "'"
	password = db.execute(strSQL)
	return password	

	
class JSONObject:  
  def __init__( self, dict ):  
      vars(self).update( dict ) 