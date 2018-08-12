from flask import Flask, render_template,  url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
#from .test import User
import os

POSTGRES_URL="127.0.0.1:5432"
POSTGRES_USER="postgres"
POSTGRES_PW="Inno@2018"
POSTGRES_DB="test"
	
db_string ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

# Define the WSGI application object
app = Flask(__name__)
app.secret_key ="8a3971a57fea4db08d86aa844e8ecefe"
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db = SQLAlchemy(app)

from src.user.views import user_blueprint
app.register_blueprint(user_blueprint,url_prefix='/v1/api')


db.create_all()

@app.route('/')
def main():
	if session.get('user'):
		return redirect('/home')
	else:
		return render_template('index.html')

@app.route('/home')
def home():
	if session.get('user'):
		return render_template('home.html')
	else:
		return redirect('/')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)