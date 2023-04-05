#test codes

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import random, requests
import pymysql
import os
import requests

### START country request 
with app.app_context():
    result = db.session.query(CovidInfo).filter(CovidInfo.country == countryname).first()

#old
    if result :
        return f'Country: {result.country} {result.data}'
        #return result
    # else:
    #     return 'no country '

    # #if not in db - get from api
    else:
        api_url = "https://api.covid19api.com/summary"
        response = requests.get(api_url)

        covid = dict() #dict with dict inside
        elem = dict() #one country information dict
        a = [] #list of country dictionaries

        get_json = response.json()
        covid = get_json.get('Countries')

        if covid:
            for key in covid:
                a.append(key) 
            
            for z in  a: 
                elem = z
                if str(elem['Country']) == str(countryname):
                    break
    #put into db
        with app.app_context():
            cntry = CovidInfo(country=str(elem['Country']), data=str('#TotalConfirmed:' + str(elem['TotalConfirmed']) + ' ' +  'NewConfirmed:' +  str(elem['NewConfirmed'])))
            db.session.add(cntry)
            db.session.commit()

    #return data to user
        info = 'Country:' +  str(elem['Country']) + '    ' +  'TotalConfirmed:' + str(elem['TotalConfirmed']) + '    ' +  'NewConfirmed:' +  str(elem['NewConfirmed'])
        return info





#OK #get country api response
# url = "https://covid-193.p.rapidapi.com/countries"
# headers = {
# 	"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
# 	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
# }
# json_reply = requests.request("GET", url, headers=headers).json()


# country_name =''
# key = "response"
# country_list = []
# country_list = json_reply.get(key)

# country_name = random.choice(country_list)

# #get country data from api

# url = "https://covid-193.p.rapidapi.com/statistics"
# headers = {
# 	"X-RapidAPI-Key": "56efe9ebf3msh1c67ba319a4de08p186620jsn17e54bc4216e",
# 	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
# }
# json_reply = requests.request("GET", url, headers=headers).json()

# response = dict()

# response = json_reply.get("response")
# country_dict = dict()
# #country_data = ''
# cases = dict()
# if response:
# 	for country in response:
# 		country_dict = country
# 		if country_dict.get("country") == country_name:
# 			cases = country_dict.get("cases")
# 			country_data = cases.get("total")
# 			break

# info = 'Country: ' + str(country_name) + ' ' + 'Total Cases: ' + str(country_data)
# print (info)



# if covid:
#     for key in covid:
#         a.append(key)

#     elem = random.choice(a)

#     info = 'Country:' +  str(elem['Country']) + '    ' +  'TotalConfirmed:' + str(elem['TotalConfirmed']) + '    ' +  'NewConfirmed:' +  str(elem['NewConfirmed'])

