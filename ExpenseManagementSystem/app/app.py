from flask import Flask
from flask import jsonify, request, session # import objects from the flask module
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask import Response

app = Flask(__name__) #define app using Flask


###############################      config information     #############################################
app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql+pymysql://root:hina@mysqlserver:3306/expensedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

################################     database model   ####################################################
db = SQLAlchemy(app)

@app.route('/')
def index():
	return "Home page"

#def dump_datetime(value):
#    """Deserialize datetime object into string form for JSON processing."""
#    if value is None:
#        return None
#    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

#database model showing the employee expense record
class ExpenseRecord(db.Model):
    __tablename__ = 'ExpenseRecord'
    expense_id = db.Column('expense_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    email = db.Column('email', db.String(50))
    category = db.Column('category', db.String(50))
    description = db.Column('description', db.String(50))
    link = db.Column('link', db.String(100))
    estimated_costs = db.Column('estimated_costs', db.Integer)
    submit_date = db.Column('submit_date', db.DateTime, default=db.func.now())
    status = db.Column('status', db.String(20))
    decision_date = db.Column('decision_date', db.DateTime)


    def __init__(self, name, email, category, description, link, estimated_costs, submit_date):
        self.name = name
        self.email = email
        self.category = category
        self.description = description
        self.link = link
        self.estimated_costs = estimated_costs
        self.submit_date = submit_date
        self.status = "pending"
#    def __repr__():
#        return self.name
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'expense_id'     : self.expense_id,
           'name'           : self.name,
           'email'          : self.email,
           'category'       : self.category,
           'description'    : self.description,
           'link'           : self.link,
           'estimated_costs': self.estimated_costs,
           'submit_date'    : self.submit_date,
           'status'         : self.status,
           'decision_date'  : self.decision_date
            }
########################################   API    #######################################################

    #          GET API that will return the employee record for the particular id
@app.route('/v1/expenses/<int:expense_id>', methods = ['GET'])
def retrieve_record(expense_id):
	record = ExpenseRecord.query.get(expense_id)
	record = ExpenseRecord.query.filter_by(expense_id=expense_id).first_or_404()
	return jsonify(result=[record.serialize])


    #          POST API that will insert employee the record for the particular id
@app.route('/v1/expenses/', methods = ['POST'])
def post_record():
	input_json = request.get_json(force = True)
	name = request.json['name']
	email = request.json['email']
	category = request.json['category']
	description = request.json['description']
	link = request.json['link']
	estimated_costs = request.json['estimated_costs']
	#submit_date = request.json['submit_date']
	submit_date = datetime.now()
	#status = "pending"
	#decision_date = datetime.now()
	#record = ExpenseRecord(name, email, category, description, link, estimated_costs, submit_date,status)
	record = ExpenseRecord(name, email, category, description, link, estimated_costs,submit_date)
	db.create_all();
	db.session.add(record)
	db.session.commit()
	record = ExpenseRecord.query.filter_by(name = name).first_or_404()
	#record = ExpenseRecord.query.get(expense_id)
	#return jsonify(result=[i.serialize for i in record.all()])
	return jsonify(result=[record.serialize]),201


    #         PUT API that will update the record for the particular id
@app.route('/v1/expenses/<int:expense_id>', methods = ['PUT'])
def put(expense_id):
	input_json = request.get_json(force = True)
	estimated_costs = request.json['estimated_costs']
	record = ExpenseRecord.query.filter_by(expense_id = expense_id).first_or_404()
	record.estimated_costs = estimated_costs
	db.session.commit()
	return "",202

    #         DELETE API that will delete the record for the particular id

@app.route('/v1/expenses/<int:expense_id>', methods =['DELETE'])
def delete(expense_id):
        record = ExpenseRecord.query.filter_by(expense_id = expense_id).delete()
        #db.session.delete(session)
        db.session.commit()
        return "",204

################################################################################

#The 404 error response in json
#@app.errorhandler(404)
#def not_found(error):
#    return (jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__" :
	db.create_all()
	app.run( host='0.0.0.0', debug = True) # run app in debug mode
