__author__ = 'eris'

import urllib
import urllib2
import logging
import json
import threading
import time
from random import randrange
logging.basicConfig(filename='decloud.log', level=logging.DEBUG)



def create_user(username):
    url = "http://localhost:8000"	    
    url += "/users/"
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"username":username})
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    r = response.read()
    logging.info(r)
    return json.loads(r)["_id"]


def create_resource(user_id, name, tags, model, description, typey, manufacturer, uri, polling_freq, creation_date, uuid,
                    active, location):
    url = "http://localhost:8000"
    url += "/resources"
    headers = {'Content-type': 'application/json'}
    data = {
#	    "user_id": user_id,
            "name": name,
#            "tags": tags,
            "description": description,
#            "type": typey,
            "manufacturer": manufacturer,
#            "uri": uri,
#            "model": model,
#            "make": "WHAT IS THIS", #TODO not in the documentation,
#            "serial": "WHAT is THIS", #TODO Not in the documentation
#            "location": location,
#            "active": active,
#            "polling_freq": polling_freq,
#            "creation_date": creation_date
    }
    req = urllib2.Request(url, json.dumps(data), headers)
    response = urllib2.urlopen(req)
    r = response.read()
    logging.info(r)
    return json.loads(r)["_id"]


def create_stream(user_id, name, tags, description, private, typey, unit,
                  accuracy, min_val, max_val, active, user_ranking, subscribers, last_updated, creation_date,
                  history_size, location):
    url = "http://localhost:8000"
    url += "/streams"
    headers = {'Content-type': 'application/json'}
    data = {"user_id": user_id,
            "name": name,
            "tags": tags,
            "description": description,
            "private": private,
            "type": typey,
            "unit": unit,
            "accuracy": accuracy,
            "min_val": min_val,
            "max_val": max_val,
#	    "polling": "false", 
#	    "uri": "http://google.de",
#	    "polling_freq": "0",
#	    "resource": "none", 
#	    "resource.resource_type": "beer",
#	    "resource.uuid":"no",
#	    "parser":"none",
#	    "data_type":"string",
#	    "location.lon":"1",
#	    "location.lat":"2",
##            "active": active,
#            "user_ranking": user_ranking,
#            "subscribers": subscribers,
#            "last_updated": last_updated,
#            "creation_date": creation_date,
#            "history_size": history_size,
            "location": location
    }
    req = urllib2.Request(url, json.dumps(data), headers)
    response = urllib2.urlopen(req)
    r = response.read()
    logging.info(r)
    return json.loads(r)["_id"]


def create_datapoint(stream_id, timestamp, value):
    #"Content-type: application/json" -d '{"timestamp" : "20131105T114543.0000", "value" : -2.5}'
    url = "http://localhost:8000"
    url += "/streams/"+stream_id+"/data"
    headers = {'Content-type': 'application/json'}
    data = {"value": value}
    req = urllib2.Request(url,json.dumps(data), headers)
    response = urllib2.urlopen(req)
    logging.info(response.read())

def read_datapoints(stream_id):
    url = "http://localhost:8000"
    url += "/streams/"+stream_id+"/data"
    response = urllib2.urlopen(url)
    h = response.read()
    return json.loads(h)


def test_single_create(create__user=False):
    if create__user:
        user_id = create_user("bieberi2")
    else:
        user_id = "bieber"
    resource_id = create_resource(user_id, "test1", "test2", "model1", "description1", "type1", "manufactur1",
                                  "http://uriforpoll.de", 20, "yesterday", "uuid", True, "Guildford")
    stream_id = create_stream(user_id,"Stream1", "temperature,celsius,Norrtalje", "Temperature in Celsius in Norrtalje",
                              "false",
                              "Temperature", "celsius", 0.95, -50.0, 50.0, "true", 10.0, 6, "2013-10-05T010502.0000",
                              "2013-10-01",
                              5000, "59.7667,18.7000")
    create_datapoint(stream_id, "20131105T114543.0000", 23)
    time.sleep(1)
    assert read_datapoints(stream_id)["data"][0]["value"] == 23.0
    print "test ok"

class _fire(threading.Thread):
    def __init__ (self, stream_id):
        threading.Thread.__init__(self)
        self.stream_id = stream_id
    def run(self): 
           
        for i in range(0,10):
            create_datapoint(self.stream_id,"bla",randrange(0,40))
#        print self.stream_id,"done"

class _read(threading.Thread):
    def __init__ (self, stream_id):
        threading.Thread.__init__(self)
        self.stream_id = stream_id
    def run(self): 
           
        for i in range(0,10):
            read_datapoints(self.stream_id)
#        print self.stream_id,"reading_done"
            
def penetration(create_user=False):
    times = []
    for scale in [1,2,3,4,5,6,7,8,9,10,50,100]:
        start = time.time()
        if create_user:
            user_id = create_user("bieber")
        else:
            user_id = "bieber"
        threads = []
        for i in range(0,scale):
                s = create_stream(user_id,"Stream1", "temperature,celsius,Norrtalje", "Temperature in Celsius in Norrtalje",
                                  "false",
                                  "Temperature", "celsius", 0.95, -50.0, 50.0, "true", 10.0, 6, "2013-10-05T010502.0000",
                                  "2013-10-01",
                                  5000, "59.7667,18.7000")
                thread_f = _fire(s)
                thread_r = _read(s)
                thread_f.start()
                thread_r.start()
                threads.append(thread_f)
                threads.append(thread_r)
                for thread in threads:
                    thread.join()
        end = time.time()
        times.append(end-start)
    from matplotlib import pyplot as plt
    plt.plot(times)
    plt.show()
penetration()
#test_single_create(True)

    
        
