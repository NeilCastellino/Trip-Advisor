import uuid
from common.database import Database
import models.hotels.constants as HotelConstants

class Hotel(object):
	def __init__(self, name, email, password, address, ph_no, card_no, total_rooms, rooms_booked, price, bank_balance = 0, user_type = "hotel", _id = None):
		self.name = name
		self.email = email
		self.password = password
		self.address = address
		self.ph_no = ph_no
		self.card_no = card_no
		self.bank_balance = float(bank_balance)
		self.total_rooms = int(total_rooms)
		self.rooms_booked = int(rooms_booked)
		self.price = float(price)
		self.user_type = user_type
		self._id = uuid.uuid4().hex if _id is None else _id

	def __repr__(self):
		return "<Hotel: {}>".format(self.name)

	def json(self):
		return{
			"_id": self._id,
			"name": self.name,
			"email": self.email,
			"password": self.password,
			"address": self.address,
			"ph_no": self.ph_no,
			"card_no": self.card_no,
			"bank_balance": self.bank_balance,
			"total_rooms": self.total_rooms,
			"rooms_booked": self.rooms_booked,
			"price": self.price,
			"user_type": self.user_type
		}

	@classmethod
	def get_by_id(cls, id):
		return cls(**Database.find_one(HotelConstants.COLLECTION, {"_id": id}))

	@classmethod
	def get_by_email(cls, email):
		return cls(**Database.find_one(HotelConstants.COLLECTION, {"email": email}))

	def save_to_mongo(self):
		Database.update(HotelConstants.COLLECTION, {'_id': self._id}, self.json())

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(HotelConstants.COLLECTION,{})]

	def delete(self):
		Database.remove(HotelConstants.COLLECTION, {"_id": self._id})

	def get_vacant_rooms(self):
		return (self.total_rooms - self.rooms_booked)

	def get_bank_balance(self):
		return self.bank_balance

	def get_price(self):
		return self.price

	def get_contents(self):
		return {
			"name": self.name,
			"email": self.email,
			"address": self.address,
			"ph_no": self.ph_no,
			"card_no": self.card_no,
			"bank_balance": self.bank_balance,
			"total_rooms": self.total_rooms,
			"rooms_booked": self.rooms_booked,
			"price": self.price,
			"user_type": self.user_type
		}