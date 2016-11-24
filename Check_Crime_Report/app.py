import logging

import operator

logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, Integer, Unicode, AnyDict
from spyne import Iterable
from spyne import json
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne.model.primitive import String
from spyne.model.complex import *
from spyne import srpc
import json
import urllib2
import datetime
import re
from operator import itemgetter, attrgetter, methodcaller


class CrimeReportService(ServiceBase):
    @rpc(float, float, float, _returns=AnyDict)
    def checkcrime(ctx, lat, lon, radius):
        # placeholder for key if needed to pass as parameter
        key = "."

        # sample url for crime api
        # crime_url ="https://api.spotcrime.com/crimes.json?lat=37.7918786&lon=-122.3688798&radius=0.12&key=."

        # base url for crime api
        base_url = "https://api.spotcrime.com/crimes.json?"
        # build url with incoming parameters
        crime_url = "%slat=%s&lon=%s&radius=%s&key=%s" % (base_url, lat, lon, radius, key)

        response = urllib2.urlopen(crime_url)
        json_response = response.read()
        jsonList = json.loads(json_response)
        crimes = jsonList['crimes'] #crimes has list of all crime records where each record is a dictionary

        totalCrime = len(crimes) # total count of crime records

        dictOfCrimeType = {} #dictionary to store the crime type
        dictOfEventTimeCounter = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0} #dictionary to store the crime time
        dictOfStreet = {} #dictionary to store street address

        # iterate over the crime records
        for crime in crimes:

            #find crime type
            crimeType = crime['type']
            if not crimeType in dictOfCrimeType: #if crime type entry is not present in dictionary then add it and set count=1
                dictOfCrimeType[crimeType] = 1
            else:                                # if crime type entry is present in dictionary then increment its count
                dictOfCrimeType[crimeType] += 1

            #find date of crime
            tempdate = crime['date']
            #obtain the time of crime in 24hour format
            crimetime = CrimeReportService.parsecrimetime(tempdate)
            #obtain the exact timespan of crime
            CrimeReportService.geteventtimeCount(crimetime, crime, dictOfEventTimeCounter=dictOfEventTimeCounter)

            #obtain the street address of crime incident
            CrimeReportService.findStreet(crime['address'], dictOfStreet)

        #create a new dictionary to store the top 3 dangerous streets
        newdictOfStreet = dict(sorted(dictOfStreet.items(), key=operator.itemgetter(1), reverse=True)[:3])
        #create a list to store the top dangerous street
        the_most_dangerous_streets = []
        #push top dangerous streets into list
        for key in newdictOfStreet:
            the_most_dangerous_streets.append(key)

        #obtain the eventTimeCounter value
        r1 = dictOfEventTimeCounter['r1'];
        r2 = dictOfEventTimeCounter['r2'];
        r3 = dictOfEventTimeCounter['r3'];
        r4 = dictOfEventTimeCounter['r4'];
        r5 = dictOfEventTimeCounter['r5'];
        r6 = dictOfEventTimeCounter['r6'];
        r7 = dictOfEventTimeCounter['r7'];
        r8 = dictOfEventTimeCounter['r8'];

        #response dictionary to store the eventTimeCounter values
        response_event_time_count = {'12:01am-3am': r1, '3:01am-6am': r2,
                            '6:01am-9am': r3, '9:01am-12noon': r4,
                            '12:01pm-3pm': r5,'3:01pm-6pm': r6,
                            '6:01pm-9pm': r7, '9:01pm-12midnight': r8}
        #response body
        responseArray = {'total_crime': totalCrime, 'the_most_dangerous_streets': the_most_dangerous_streets,
                         'crime_type_count': dictOfCrimeType,
                         'event_time_count': response_event_time_count}
        return responseArray

    #function to convert
    @staticmethod
    def parsecrimetime(crimedate):
        # convert datetime string (month, day, year, hour, minute, am/pm) to (year, month, date, 24 hr format, minute)
        dt = datetime.datetime.strptime(crimedate, "%m/%d/%y %I:%M %p")
       # ti = dt.time() #obtain (24 hr format, minute)
        return dt

    @staticmethod
    def findStreet(address, dictOfStreet):
        match1 = re.search(r'[\d\w\s]+[BLOCKF\s]+ ([\w\s\d]+[AVBLDRIENUSTN]+)', address, re.IGNORECASE)
        if match1:
            street = match1.group(1)

            if not street in dictOfStreet:
                dictOfStreet[street] = 1
            else:
                dictOfStreet[street] = dictOfStreet[street] + 1
            return dictOfStreet

        match2 = re.search(r'([\d\w\s]+ST) & ([\w\s\d]+ST)', address, re.IGNORECASE)
        if match2:
            street1 = match2.group(1)
            street2 = match2.group(2)
            if not street1 in dictOfStreet:
                dictOfStreet[street1] = 1
            else:
                dictOfStreet[street1] = dictOfStreet[street1] + 1

            if not street2 in dictOfStreet:
                dictOfStreet[street2] = 1
            else:
                dictOfStreet[street2] = dictOfStreet[street2] + 1

            return dictOfStreet

        match3 = re.search(r'([\w\s\d]+[AVBLDRIENUSTN]+)', address, re.IGNORECASE)
        if match3:
            street = match3.group(1)
            if not street in dictOfStreet:
                dictOfStreet[street] = 1
            else:
                dictOfStreet[street] = dictOfStreet[street] + 1

            return dictOfStreet


    @staticmethod
    def geteventtimeCount(crimetime, crime, dictOfEventTimeCounter):
        year = crimetime.year
        month = crimetime.month
        day = crimetime.day
        #set the time slots for comparison to categorize the crime event time
        date1 = datetime.datetime(year, month, day, 00, 01, 00)
        date2 = datetime.datetime(year, month, day, 03, 00, 00)

        #if the crimetime matches the slots increase the counter for the slot
        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r1'] = dictOfEventTimeCounter['r1'] + 1
            return dictOfEventTimeCounter

        date1 = datetime.datetime(year, month, day, 03, 01, 00)
        date2 = datetime.datetime(year, month, day, 06, 00, 00)

        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r2'] = dictOfEventTimeCounter['r2'] + 1
            return dictOfEventTimeCounter

        date1 = datetime.datetime(year, month, day, 06, 01, 00)
        date2 = datetime.datetime(year, month, day, 9, 1, 00)

        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r3'] = dictOfEventTimeCounter['r3'] + 1
            return dictOfEventTimeCounter

        date1 = datetime.datetime(year, month, day, 9, 01, 00)
        date2 = datetime.datetime(year, month, day, 12, 1, 00)

        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r4'] = dictOfEventTimeCounter['r4'] + 1
            return dictOfEventTimeCounter

        date1 = datetime.datetime(year, month, day, 12, 01, 00)
        date2 = datetime.datetime(year, month, day, 15, 00, 00)

        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r5'] = dictOfEventTimeCounter['r5'] + 1
            return dictOfEventTimeCounter

        date1 = datetime.datetime(year, month, day, 15, 01, 00)
        date2 = datetime.datetime(year, month, day, 18, 00, 00)

        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r6'] = dictOfEventTimeCounter['r6'] + 1
            return dictOfEventTimeCounter

        date1 = datetime.datetime(year, month, day, 18, 01, 00)
        date2 = datetime.datetime(year, month, day, 21, 00, 00)

        if date1 <= crimetime <= date2:
            dictOfEventTimeCounter['r7'] = dictOfEventTimeCounter['r7'] + 1
            return dictOfEventTimeCounter

        dictOfEventTimeCounter['r8'] = dictOfEventTimeCounter['r8'] + 1

        return dictOfEventTimeCounter


application = Application([CrimeReportService], tns='hina.sjsu.lab2',in_protocol=HttpRpc(validator='soft'),out_protocol=JsonDocument())

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.

    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
