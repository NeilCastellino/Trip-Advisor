import uuid
from common.database import Database
import models.contacts.constants as ContactConstants

class Contact(object):
	def __init__(self, name, email, message, _id=None):
		self.name = name
		self.email = email
		self.message = message
		self._id = uuid.uuid4().hex if _id is None else _id

	@staticmethod
	def save_contact(contact):
		Database.insert(ContactConstants.CONTACT, contact)

	@classmethod
	def all_contacts(cls):
		return [cls(**elem) for elem in Database.find(ContactConstants.CONTACT,{})]