from flask import redirect, session, g, url_for, request, flash, render_template, Blueprint
from fms import app

main_blueprint = Blueprint('main_blueprint', __name__)
						
@main_blueprint.route('/')
def main():
	if session.get('user_id'):
		return redirect('/home')
	else:
		return render_template('index.html')

@main_blueprint.route('/home')
def home():
	if session.get('user_id'):
		return render_template('home.html')
	else:
		return redirect('/')
