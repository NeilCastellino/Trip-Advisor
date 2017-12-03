from flask import Blueprint, request, session, url_for, render_template, redirect
from werkzeug.utils import redirect
from models.users.user import User
from models.hotels.hotel import Hotel
from models.airlines.airline import Airline
import models.users.errors as UserErrors
import models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods = ['POST', 'GET'])
def login_user():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			if User.is_login_valid(email, password):
				session['email'] = email
				user = User.find_by_email(email)
				return render_template("home.html", user = user)
		except UserErrors.UserError as e:
			return e.message
	return render_template("users/login.html")

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		address = request.form['address']
		ph_no = request.form['ph_no']
		card_no = request.form['card_no']
		try:
			if User.register_user(email, password, name, address, ph_no, card_no):
				session['email'] = email
				return redirect(url_for(".user_dashboard"))
		except UserErrors.UserError as e:
			return e.message
	return render_template("users/register.html")

@user_blueprint.route('/dashboard')
def user_dashboard():
	user = User.find_by_email(session['email'])
	contents = user.get_contents()
	return render_template('users/dashboard.html', contents=contents)

@user_blueprint.route('/logout')
def logout_user():
	session['email'] = None
	return redirect(url_for('home'))

@user_blueprint.route('/contact', methods=['GET', 'POST'])
def contact_us():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		message = request.form['message']

		contact = {
			"name": name,
			"email": email,
			"message": message
		}
		User.save_contact(contact)
		return redirect(url_for('home'))
	return render_template("users/contact.html")