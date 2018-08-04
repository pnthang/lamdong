from flask import Blueprint
from flask import Flask, abort, request, jsonify
import json
from flask import jsonify
from .modules.user.dbUtils import DbUtils

User = Blueprint('User',__name__)

@User.route('/user/add',methods=['POST'])
def addfilm():	
	# read the posted values from the UI
	_title = request.form['title']
	_director = request.form['director']
	_year = request.form['year']
	
    # validate the received values
	if (_title and _director and _year):
		dbUtils = DbUtils()
		dbUtils.addNewUser(_title,_director,_year)
		return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	#if not request.get_json(force=True):
	#	abort(400)			

@User.route('/user/get',methods=['GET'])
def getFilms():  
    films = []  
    dbUtils = DbUtils()  
    filmData = dbUtils.getUsers()  
    for r in filmData:    
        a = {"title": r[0], "director": r[1], "year":r[2]}  
        films.append(a)  
      
    return jsonify(films) 

@User.route('/user/create_table')  
def createFilmTable():  
    dbUtils = DbUtils()  
    dbUtils.createTable();  
    result = {"result": "Users Table Created"}  
    return jsonify(result) 

	

	
class JSONObject:  
  def __init__( self, dict ):  
      vars(self).update( dict ) 