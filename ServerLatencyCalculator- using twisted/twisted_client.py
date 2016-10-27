from __future__ import print_function

from pprint import pformat

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from datetime import datetime
import time
import thread
import threading
import operator

"""class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            #print('Some data received:')
            #print(display)
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())
        self.finished.callback(None)"""

#lst = ('http://www.msn.com','http://www.hotmail.com')
lst = ('http://localhost:3000/checkcrime','http://localhost:3001/checkcrime')

dict = {}


for x in lst:
    dict[x]=[x,0,0,0]

a_lock = threading.Lock()

#urlarr =>tuple(url,reqtime)
def cbRequest(response,urlarr):
    print("********************************************************")
    # print('Response version:', response.version)
    # print('Response code:', response.code)
    # print('Response phrase:', response.phrase)
    #print('Response headers:')
    resTime = datetime.now()
    rqt =urlarr[1]
    url =urlarr[0]
    dt =dict
    dt[url]=[url,rqt,resTime,0] #url,req time, res time, latency

def funcrequrl():
    for url in lst:
        reqTime = datetime.now()
        print("Request time for "+url+" : "+str(reqTime))
        dict[url] = [reqTime,0,url]
        #List.append(dict)
        agent = Agent(reactor)
        d = agent.request('GET', url, Headers({'User-Agent': ['Twisted Web Client Example']}),None)
        d.addCallback(cbRequest,[url,reqTime])

    d.addBoth(cbShutdown)

def printd():
    time.sleep(5)
    print ("*Dictionary data - Start *")

    for x in dict.iterkeys():
        b =dict[x]
        _url = b[0]
        _rqtime = b[1]
        print(_rqtime)
        _restime = b[2]
        print (_restime)
        _latency = _restime - _rqtime
        b[3] =_latency
        print ("URL : "+str(_url)+', '+" Req Time : "+str(_rqtime)+", Res time :  "+str(_restime) + ", Latency : "+str(_latency))
    print("*Dictionary data  End *")

    _smallestLatencyURL = dict.keys()[0]
    _list = dict[_smallestLatencyURL]
    _smallestLatency = _list[3]
    print("first url :" + _smallestLatencyURL + "  latency : " + str(_smallestLatency))

    for x in dict.iterkeys():
        b = dict[x]
        if(_smallestLatency > b[3]):
            _smallestLatencyURL = b[0]
            _smallestLatency = b[3]

    print("smallest latency url :" + _smallestLatencyURL + "  latency : " + str(_smallestLatency))

    """sort(dict.values(), key=operator.itemgetter(2))
    print("*Dictionary data - Start *")
    for x in dict.iterkeys():
        b = dict[x]
        _url = b[0]
        _rqtime = b[1]
        _restime = b[2]
        _latency = b[3]
        print("URL : " + str(_url) + ', ' + " Req Time : " + str(_rqtime) + ", Res time :  " + str(_restime) + ", Latency : " + str(_latency))
    print("*Dictionary data  End *")

    _smallestLatency
    data_sorted = sorted(dict, key=lambda item: item[3])
    print(data_sorted)"""
def cbShutdown(ignored):
    reactor.stop()

threading.Thread(target=funcrequrl).start()
threading.Thread(target=printd).start()

reactor.run()