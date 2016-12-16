from flask import Flask
from consistentHashing import *
import httplib
import json


def create_HashRing():
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


def getUserInput():

    #hash all the application nodes
    ch = create_HashRing()
    while 1:

        # get user data
        id = raw_input("Enter id : ")
        name = raw_input("Enter name : ")
        email = raw_input("Enter email : ")
        category = raw_input("Enter category : ")
        link = raw_input("Enter link : ")
        description = raw_input("Enter description : ")
        estimated_costs = raw_input("Enter estimated_costs : ")
        submit_date = raw_input("Enter submit_date : ")

        #create request json body
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

        # hash the request object id to obtain the target node url
        target_nodeUrl = ch.__getitem__(id)
        print target_nodeUrl
        # estabish connection with the target url
        connection = httplib.HTTPConnection(target_nodeUrl)
        headers = {'Content-type': 'application/json'}
        connection.request('POST', '/v1/expenses/', json_req, headers)
        response = connection.getresponse()
        print(response.read().decode())


if __name__ == "__main__":
    getUserInput()