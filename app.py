from flask import Flask, render_template, request
#from get_country import get_random_info, get_country_info
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import random, requests
import pymysql
import os

app = Flask(__name__)

# #database connection info
# def db_connect():
# db_username = 'tester'
# db_password = 'pass'
# db_name = 'covid_db'
# db_host = 'localhost'
# connect = 'mysql+pymysql://'+db_username+':'+db_password+'@'+db_host+'/'+db_name
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
connect = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_NAME
# 	return connect
# #from my_config import db_connect
# connect = db_connect()

# #create db if not exist
# engine = create_engine(connect)
# if not database_exists(engine.url):
# 	create_database(engine.url)

# create the extension
db = SQLAlchemy()

# configure the SQL database, relative to the app instance folder
#!!!!!!!!!!
app.config["SQLALCHEMY_DATABASE_URI"] = connect

# initialize the app with the extension
db.init_app(app)
# with app.app_context():
#     db.create_all()

#db model description
class CovidInfo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	country = db.Column(db.String(50), unique=True)
	data = db.Column(db.String(250))

	def __init__(self, country, data):
		self.country = country
		self.data = data

#create the table if not exist
with app.app_context():
	db.create_all()


### functions

### START random request for root url
def get_random_info():
	url = "https://covid-193.p.rapidapi.com/countries"
	headers = {
		"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
		"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
	}
	json_reply = requests.request("GET", url, headers=headers).json()

#   country_name =''
	key = "response"
	country_list = []
	country_list = json_reply.get(key)

	country_name = random.choice(country_list)

	#get country data from api

	url = "https://covid-193.p.rapidapi.com/statistics"
	# headers = {
	# 	"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
	# 	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
	# }
	json_reply = requests.request("GET", url, headers=headers).json()

	response = dict()

	response = json_reply.get("response")
	country_dict = dict()
	#country_data = ''
	cases = dict()
	if response:
		for country in response:
			country_dict = country
			if country_dict.get("country") == country_name:
				cases = country_dict.get("cases")
				country_data = cases.get("total")
				break

		info = 'RANDOM Country: ' + str(country_name) + ' ' + 'Total Cases: ' + str(country_data)
	else:
		info = 'ERROR: cant get information from API'
	return info
### END random request for root url



### START country request 
def get_country_info(country_name):
#	app = Flask(__name__)
	with app.app_context():
		result = db.session.query(CovidInfo).filter(CovidInfo.country == country_name).first()
		if result :
			return f'Country: {result.country} Total cases: {result.data} (CACHED INFO)'
		else:
			url = "https://covid-193.p.rapidapi.com/statistics"
			headers = {
				"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
				"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
			}
			json_reply = requests.request("GET", url, headers=headers).json()

			#response = [] #list of dict()

			response = json_reply.get("response")
			country_dict = dict()
			cases = dict()
			if response:
				#check country
				is_present = False
				country_temp = dict()
				for check in response:
					country_temp = check
					if country_temp.get("country") == country_name:
						is_present =True
				#if check ok
				if is_present: 
					for country in response:
						country_dict = country
						if country_dict.get("country") == country_name:
							cases = country_dict.get("cases")
							country_data = cases.get("total")
							#put into db
							with app.app_context():
								cntry = CovidInfo(country=country_name, data=country_data)
								db.session.add(cntry)
								db.session.commit()
							break
					info = 'Country: ' + str(country_name) + ' ' + 'Total Cases: ' + str(country_data) + ' (ACTUAL)'
				else:
					info = 'ERROR. There is no such country - '+ country_name +'.   Check URL or country name. Example: Sudan, Turks-and-Caicos '
			else: 
				info = 'ERROR: cant get information from API'
			return info
### END country request




#MAIN CODE
@app.route('/')
def index():
	obj = get_random_info()
	return render_template('index.html',data=obj)

#per country info
@app.route('/info', methods=['GET'])
def index2():
	#country_name = str.capitalize(request.args.get('country'))
	country_name = str(request.args.get('country'))
	obj = get_country_info(country_name)
	return render_template('index.html',data=obj)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



