import random, requests
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database



def country_info(countryname):
    #create db if not exist
    engine = create_engine("mysql+pymysql://covid:pass@localhost/covid")
    if not database_exists(engine.url):
        create_database(engine.url)
    #print(database_exists(engine.url))

    # create the extension
    db = SQLAlchemy()

    # create the app
    app = Flask(__name__)

    #socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

    # configure the SQL database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://covid:pass@localhost/covid' #+ socket
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # initialize the app with the extension
    db.init_app(app)

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

#upper lines are ok

    #ask db 
    #if counrty in db - get it 

    # def test_connection(self):
    with app.app_context():
        #result = db.session.query(CovidInfo).where(CovidInfo.country == 'Wacanda').all()
        #result = db.session.execute(db.select(CovidInfo.country, CovidInfo.data).where(CovidInfo.country == countryname)).all()
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
    return ''