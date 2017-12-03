from flask import Blueprint, request, render_template, redirect, url_for, session
import uuid
from models.airlines.airline import Airline
from models.flights.flight import Flight
from models.users.user import User
import models.users.decorators as user_decorators

flight_blueprint = Blueprint('flights', __name__)

@flight_blueprint.route('/')
def index():
	flights = Flight.all()
	return render_template('flights/flight_index.html', flights=flights)

@flight_blueprint.route('/flight_view/<string:airline_name>')
def flight_page(airline_name):
	flight = Flight.get_by_airline_id(airline_name)
	return render_template("flights/flight.html", flight = flight)

@flight_blueprint.route('/add_flights', methods=['GET', 'POST'])
@user_decorators.requires_login
def flight_add():
	if request.method == 'POST':
		plane_no = request.form['plane_no']
		source = request.form['source']
		destination = request.form['destination']
		plane_timing = request.form['plane_timing']
		total_seats = int(request.form['total_seats'])
		seats_booked = int(request.form['seats_booked'])
		airline_name = request.form['airline_name']
		price = float(request.form['price'])

		Flight(plane_no, source, destination, plane_timing, total_seats, seats_booked, airline_name, price).save_to_mongo()
		return redirect(url_for(".index"))
	return render_template('flights/new_flight.html')

@flight_blueprint.route('/delete/<string:flight_id>')
@user_decorators.requires_login
def delete_flight(flight_id):
	Flight.get_by_id(flight_id).delete()
	return redirect(url_for('.index'))

@flight_blueprint.route('/booking_flight/<string:flight_id>', methods=['GET', 'POST'])
def flight_book(flight_id):
	flights = Flight.get_by_id(flight_id)
	if request.method == 'POST':
		plane_no = flights.plane_no
		price = float(flights.price)
		tickets = int(request.form['rooms'])
		total = price * tickets
		flights.seats_booked += tickets
		airline_name = flights.airline_name
		airline = Airline.get_by_name(airline_name)
		airline.bank_balance += total
		flights.save_to_mongo()
		airline.save_to_mongo()
		order = {
			"Plane_no": plane_no,
			"price": price,
			"tickets": tickets,
			"total": total
		}
		user = User.find_by_email(session['email'])
		user.orders = {uuid.uuid4().hex : order}
		user.points_earned += (price/100)
		user.save_to_mongo()
		return redirect(url_for('users.user_dashboard'))
	return render_template('flight_book.html', flights = flights)