from flask import Flask, render_template,  url_for, redirect, session
from .test import User


# Define the WSGI application object
app = Flask(__name__)

app.secret_key ="8a3971a57fea4db08d86aa844e8ecefe"

app.register_blueprint(User,url_prefix='/v1/api/user')

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

#def service():
#	return "Service is running!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)