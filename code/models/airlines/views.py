from flask import Blueprint, render_template, request, redirect, url_for, session
from models.airlines.airline import Airline
from models.users.user import User
import models.users.decorators as user_decorators
import uuid

airline_blueprint = Blueprint('airlines', __name__)

@airline_blueprint.route('/')
def index():
	airlines = Airline.all()
	return render_template('airlines/airline_index.html', airlines=airlines)

@airline_blueprint.route('/airline/<string:airline_id>')
def airline_page(airline_id):
	return render_template('airlines/airline.html', airline = Airline.get_by_id(airline_id))

@airline_blueprint.route('/delete/<string:airline_id>')
@user_decorators.requires_admin_permissions
def delete_airline(airline_id):
	Airline.get_by_id(airline_id).delete()
	return redirect(url_for('.index'))

@airline_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def create_airline():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		address = request.form['address']
		ph_no = request.form['ph_no']
		card_no = request.form['card_no']

		Airline(name, email, password, address, ph_no, card_no).save_to_mongo()
		return redirect(url_for('.index'))
	return render_template('airlines/new_airline.html')