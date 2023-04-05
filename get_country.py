#get country info functions
import random, requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import random, requests
import pymysql
import os

#db model description
class CovidInfo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	country = db.Column(db.String(50), unique=True)
	data = db.Column(db.String(250))

	def __init__(self, country, data):
		self.country = country
		self.data = data

		
### START random request for root url
def get_random_info():
	url = "https://covid-193.p.rapidapi.com/countries"
	headers = {
		"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
		"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
	}
	json_reply = requests.request("GET", url, headers=headers).json()

#	country_name =''
	key = "response"
	country_list = []
	country_list = json_reply.get(key)

	country_name = random.choice(country_list)

	#get country data from api

	url = "https://covid-193.p.rapidapi.com/statistics"
	headers = {
		"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
		"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
	}
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
	app = Flask(__name__)
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

			response = dict()

			response = json_reply.get("response")
			country_dict = dict()
			cases = dict()
			if response:
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
				info = 'ERROR: cant get information from API'
			return info
### END country request