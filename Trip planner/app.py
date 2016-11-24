# coding=utf-8
import urllib2

from flask import Flask, render_template
from flask import jsonify, request, session # import objects from the flask module
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy import event
from sqlalchemy import DDL
import requests
from flask import Response

app = Flask(__name__) #define app using Flask


#************************************  database config information    ********************************#
#app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql+pymysql://root:hina@mysqlserver:3306/expensedb'
app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql+pymysql://hina:hina@127.0.0.1:3306/address'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#**********************************   database model  ************************************************#
db = SQLAlchemy(app)

class LocationDetails(db.Model):
    __tablename__ = 'LocationDetails'
    location_id = db.Column('location_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    address = db.Column('address', db.String(50))
    city = db.Column('city', db.String(30))
    state = db.Column('state', db.String(30))
    zip = db.Column('zip', db.String(10))
    createdOn = db.Column('createdOn', db.DateTime, default=db.func.now())
    updatedOn = db.Column('updatedOn', db.DateTime, default=db.func.now())
    lat = db.Column('lat', db.FLOAT)
    lng = db.Column('lng', db.FLOAT)

    def __init__(self, name, address,city, state, zip, createdOn, updatedOn, lat, lng):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.createdOn = createdOn
        self.updatedOn = updatedOn
        self.lat = lat
        self.lng = lng

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.location_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'coordinate': {'lat': self.lat,'lng': self.lng}
        }
#****************************************CRUST API*********************************************#
#***************************************    GET ***********************************************#

@app.route('/v1/locations/<int:location_id>', methods = ['GET'])
def retrieve_record(location_id):
	record = LocationDetails.query.get(location_id)
	record = LocationDetails.query.filter_by(location_id=location_id).first_or_404()
	return jsonify(result=[record.serialize])
#*****************************************  POST **********************************************#

@app.route('/v1/locations/', methods=['POST'])
def post_location():
    input_json = request.get_json(force=True)
    name = request.json['name']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']
    createdOn = datetime.now()
    updatedOn = datetime.now()

    print(name)
    print(address)
    print(city)
    print(state)
    print(zip)

    url = ("http://maps.google.com/maps/api/geocode/json?address="+name+",+"+address+",+"+city+",+"+state+",+"+zip+"&sensor=false")
    req_url = url.replace(" ","+")
    response = urllib2.urlopen(req_url)
    json_response = response.read()
    jsonList = json.loads(json_response)
    lat = jsonList["results"][0]["geometry"]["location"]["lat"]
    lng = jsonList["results"][0]["geometry"]["location"]["lng"]
    print(lat)
    print(lng)

    record = LocationDetails(name,address,city,state,zip,createdOn, updatedOn, lat, lng)
    #db.create_all();
    db.session.add(record)
    db.session.commit()
    record = LocationDetails.query.filter_by(name=name).first_or_404()
    return jsonify(result=[record.serialize]), 201

#**********************************************  PUT ***********************************************#
#         PUT API that will update the location for the particular location_id
@app.route('/v1/locations/<int:location_id>', methods = ['PUT'])
def put(location_id):
	input_json = request.get_json(force = True)
	name = request.json['name']
	record = LocationDetails.query.filter_by(location_id = location_id).first_or_404()
	record.name = name
	db.session.commit()
	return "",202

#******************************************* DELETE  ***********************************************#
#       DELETE API that will delete the location for the particular location_id

@app.route('/v1/locations/<int:location_id>', methods =['DELETE'])
def delete(location_id):
        record = LocationDetails.query.filter_by(location_id = location_id).delete()
        #db.session.delete(session)
        db.session.commit()
        return "",204


#***************************************code for user interface*************************************#

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/result',methods = ['POST'])
def getPrice():
    input= json.dumps(request.json)
    data = input
    print(data)
    return "success"



#************************************run the main program**************************************#

if __name__ == "__main__" :
    db.create_all()
    event.listen(LocationDetails.__table__,"after_create",DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;"))
    app.run( host='0.0.0.0',port = 5000, debug = True) # run app in debug mode
