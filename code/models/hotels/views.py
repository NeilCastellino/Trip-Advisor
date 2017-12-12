from flask import Blueprint, render_template, request, redirect, url_for, session
from models.hotels.hotel import Hotel
from models.users.user import User
import models.users.decorators as user_decorators
import models.hotels.errors as UserErrors
import json
import datetime
import uuid

hotel_blueprint = Blueprint('hotels', __name__)

@hotel_blueprint.route('/')
def index():
	hotels = Hotel.all()
	return render_template('hotels/hotel_index.html', hotels=hotels)

@hotel_blueprint.route('/hotel/<string:hotel_id>')
def hotel_page(hotel_id):
	return render_template('hotels/hotel.html', hotel = Hotel.get_by_id(hotel_id))

@hotel_blueprint.route('/delete/<string:hotel_id>')
@user_decorators.requires_admin_permissions
def delete_hotel(hotel_id):
	Hotel.get_by_id(hotel_id).delete()
	return redirect(url_for('.index'))

@hotel_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def create_hotel():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		address = request.form['address']
		ph_no = request.form['ph_no']
		card_no = request.form['card_no']
		total_rooms = request.form['total_rooms']
		rooms_booked = request.form['rooms_booked']
		price = request.form['price']

		Hotel(name, email, password, address, ph_no, card_no, total_rooms,rooms_booked, price).save_to_mongo()
		return redirect(url_for('.index'))
	return render_template('hotels/new_hotel.html')

@hotel_blueprint.route('/booking_hotel/<string:hotel_id>', methods=['GET', 'POST'])
def hotel_book(hotel_id):
	hotels = Hotel.get_by_id(hotel_id)
	if request.method == 'POST':
		name = hotels.name
		price = float(hotels.price)
		date_to = request.form['date-to']
		date_from = request.form['date-from']
		rooms = int(request.form['rooms'])
		days = int(request.form['days'])
		total = price * rooms * days
		
		if hotels.total_rooms <= rooms:
			try:
				Hotel.is_hotel_full()
			except UserErrors.UserError as e:
				return e.message

		for k,v in hotels.dates.items():
			count = days
			while count >= 0:
				tr = 0
				strD = date_from[:-2]
				day = int(date_from[8:])
				day += count
				day1 = str(day)
				strD += day1
				if k == strD:
					for m in hotels.dates[k]:
						for k,v in m.items():
							tr += v
							if hotels.total_rooms <= tr:
								try:
									Hotel.is_hotel_full()
								except UserErrors.UserError as e:
									return e.message
				count -= 1
		hotels.bank_balance += total
		hotels.save_to_mongo()
		order = {
			"hotel_name": name,
			"price": price,
			"rooms": rooms,
			"days": days,
			"total": total,
			"date_to": date_to,
			"date_from": date_from
		}
		user = User.find_by_email(session['email'])
		user.orders = {uuid.uuid4().hex : order}
		user.points_earned += (price/100)
		user.save_to_mongo()

		count = days
		while count >= 0:
			strD = date_from[:-2]
			day = int(date_from[8:])
			day += count
			day1 = str(day)
			strD += day1
			if strD in hotels.dates:
				diction = {user.name: rooms}
				hotels.dates[strD].append(diction)
			else:
				summary = {user.name: rooms}
				hotels.dates[strD] = []
				hotels.dates[strD].insert(0, summary)
			count -= 1
			hotels.save_to_mongo()
		return redirect(url_for('users.user_dashboard'))
	return render_template('hotel_book.html', hotels = hotels)
