from flask import Flask, render_template, request, session
from common.database import Database
from models.users.user import User

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"

@app.before_first_request
def init_db():
	Database.initialize()

@app.route('/')
def home():
	return render_template("home.html")

from models.users.views import user_blueprint
from models.hotels.views import hotel_blueprint
from models.airlines.views import airline_blueprint
from models.flights.views import flight_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(hotel_blueprint, url_prefix="/hotels")
app.register_blueprint(flight_blueprint, url_prefix="/flights")
app.register_blueprint(airline_blueprint, url_prefix="/airlines")