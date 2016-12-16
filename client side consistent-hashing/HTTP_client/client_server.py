from flask import Flask
import httplib
import json
from flask import request
from flask import jsonify
from consistentHashing import *

app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello Harshada!"
    
def createHashRing():
    ch = ConsistentHashRing()
    node1_req_url = "192.168.99.100:3001"
    node2_req_url = "192.168.99.100:3002"
    node3_req_url = "192.168.99.100:3003"
    node1name = "node1"
    node2name = "node2"
    node3name = "node3"
    ch.__setitem__(node1name, node1_req_url)
    ch.__setitem__(node2name, node2_req_url)
    ch.__setitem__(node3name, node3_req_url)
    return ch

def acceptUserInput():
    while 1:
        #accepting user input
        id = raw_input("Enter id : ")
        name = raw_input("Enter name : ")
        email = raw_input("Enter email : ")
        category = raw_input("Enter category : ")
        link = raw_input("Enter link : ")
        description = raw_input("Enter description : ")
        estimated_costs = raw_input("Enter estimated_costs : ")
        submit_date = raw_input("Enter submit_date : ")
        req_body = {
            "id": int(id),
            "name": str(name),
            "email": str(email),
            "category": str(category),
            "link": str(link),
            "description": str(description),
            "estimated_costs": str(estimated_costs),
            "submit_date": str(submit_date)
        }
        
        json_req = json.dumps(req_body)
        print json_req
        #getting hashed node
        nodeUrl = ch.__getitem__(id)
        connection = httplib.HTTPConnection(nodeUrl)
        headers = {'Content-type': 'application/json'}
        connection.request('POST', '/v1/expenses', json_req, headers)
        response = connection.getresponse()
        print(response.read())
        
        
    
ch = createHashRing()        

@app.route('/expenseHash', methods=['POST'])
def addExpense():
    object = json.loads(request.data)
    req_body = {
        "id": object['id'],
        "name": object['name'],
        "email": object['email'],
        "category": object['category'],
        "link": object['link'],
        "description": object['description'],
        "estimated_costs": object['estimated_costs'],
        "submit_date": object['submit_date']
    }
    
    json_req = json.dumps(req_body)
    print json_req
    #getting hashed node
    nodeUrl = ch.__getitem__(object['id'])
    print nodeUrl
    connection = httplib.HTTPConnection(nodeUrl)
    headers = {'Content-type': 'application/json'}
    connection.request('POST', '/v1/expenses/', json_req, headers)
    response = connection.getresponse()
    print(response.read().decode())
    resp = jsonify(response.read().decode())
    return resp
    
if __name__ == "__main__":
    #global ch = createHashRing()
    app.run(debug=True,host='0.0.0.0')