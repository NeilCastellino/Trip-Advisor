import uuid
from common.database import Database
import models.airlines.constants as AirlineConstants

class Airline(object):
	def __init__(self, name, email, password, address, ph_no, card_no, user_type = "airline", bank_balance = 0, _id = None):
		self.name = name
		self.email = email
		self.password = password
		self.address = address
		self.ph_no = ph_no
		self.card_no = card_no
		self.user_type = user_type
		self.bank_balance = bank_balance
		self._id = uuid.uuid4().hex if _id is None else _id

	def __repr__(self):
		return "<Airline: {}>".format(self.name)

	def json(self):
		return{
			"_id": self._id,
			"name": self.name,
			"email": self.email,
			"password": self.password,
			"address": self.address,
			"ph_no": self.ph_no,
			"user_type": self.user_type,
			"card_no": self.card_no,
			"bank_balance": self.bank_balance
		}

	@classmethod
	def get_by_id(cls, id):
		return cls(**Database.find_one(AirlineConstants.COLLECTION, {"_id": id}))

	def save_to_mongo(self):
		Database.update(AirlineConstants.COLLECTION, {'_id': self._id}, self.json())

	@classmethod
	def get_by_name(cls, airline_name):
		return cls(**Database.find_one(AirlineConstants.COLLECTION, {"name": airline_name}))

	@classmethod
	def get_by_user_type(cls):
		return cls(**Database.find_one(AirlineConstants.COLLECTION, {"user_type": "airline"}))

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(AirlineConstants.COLLECTION,{})]

	def delete(self):
		Database.remove(AirlineConstants.COLLECTION, {"_id": self._id})

	def get_bank_balance(self):
		return self.bank_balance

	def get_contents(self):
		return {
			"name": self.name,
			"email": self.email,
			"address": self.address,
			"ph_no": self.ph_no,
			"user_type": self.user_type,
			"card_no": self.card_no,
			"bank_balance": self.bank_balance
		}