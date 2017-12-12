from common.database import Database
import models.flights.constants as FlightConstants
import uuid
import models.flights.errors as UserErrors

class Flight(object):
	def __init__(self, plane_no, source, destination, plane_timing, total_seats, seats_booked, airline_name, price, dates={}, _id = None):
		self.plane_no = plane_no
		self.source = source
		self.destination = destination
		self.plane_timing = plane_timing
		self.total_seats = int(total_seats)
		self.seats_booked = int(seats_booked)
		self.airline_name = airline_name
		self.price = price
		self.dates = dates
		self._id = uuid.uuid4().hex if _id is None else _id

	def __repr__(self):
		return "<Plane: {} to {}>".format(self.plane_no, self.destination)

	def save_to_mongo(self):
		Database.update(FlightConstants.COLLECTION, {"_id": self._id}, self.json())

	def json(self):
		return {
			"plane_no": self.plane_no,
			"source": self.source,
			"destination": self.destination,
			"plane_timing": self.plane_timing,
			"total_seats": self.total_seats,
			"seats_booked": self.seats_booked,
			"airline_name": self.airline_name,
			"_id": self._id,
			"price": self.price,
			"dates": self.dates
		}

	@classmethod
	def get_by_id(cls, item_id):
		return cls(**Database.find_one(FlightConstants.COLLECTION, {"_id": item_id}))

	@classmethod
	def get_by_airline_id(cls, airline_name):
		return [cls(**elem) for elem in Database.find(FlightConstants.COLLECTION, {"airline_name": airline_name})]

	def get_vacant_seats(self):
		return (self.total_seats - self.seats_booked)

	def get_price(self):
		return self.price

	def delete(self):
		Database.remove(FlightConstants.COLLECTION, {"_id": self._id})

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(FlightConstants.COLLECTION,{})]

	@staticmethod
	def is_flight_full():
		raise UserErrors.FlightFull("Sorry! All the seats are full")