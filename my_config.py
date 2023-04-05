#my config

#database connection info
def db_connect():
	db_username = 'tester'
	db_password = 'pass'
	db_name = 'covid_db'
	db_host = 'localhost'
	connect = 'mysql+pymysql://'+db_username+':'+db_password+'@'+db_host+'/'+db_name
	return connect


# #db model description
# class CovidInfo(db.Model):
# #class CovidInfo():
#	 id = db.Column(db.Integer, primary_key = True)
#	 country = db.Column(db.String(50), unique=True)
#	 data = db.Column(db.String(250))

#	 def __init__(self, country, data):
#		 self.country = country
#		 self.data = data