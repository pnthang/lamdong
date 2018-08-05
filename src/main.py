from flask import Flask, render_template,  url_for
from .users.controller import User


# Define the WSGI application object
app = Flask(__name__)

app.register_blueprint(User,url_prefix='/v1/api')

@app.route('/')
def main():	
    return render_template('index.html')

@app.route('/showAddFilm')
def showAddFilm():
    return render_template('film.html')

#def service():
#	return "Service is running!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)