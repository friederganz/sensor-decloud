__author__ = 'Daniel'
import urllib2
import urllib
import json
from pprint import pprint
from httplib2 import Http
from unicodedata import normalize
from datetime import datetime
import pika

#specify hostname by name or ip adress
def establishConnection(hostname='127.0.0.1'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(hostname))
    return connection


# ,"limit":2
def importData(url, resource):
    data_string = urllib.quote(json.dumps({'resource_id': resource}))
    response = urllib2.urlopen(url,data_string)
    assert response.code == 200

    response_dict = json.loads(response.read())
    assert response_dict['success'] is True
    result = response_dict['result']
    # pprint(result)
    return result["records"]

def splitInStreams(data):
    streams ={}
    #ugly hack
    first = True
    for arr in data:
        for key in arr:
            #ugly hack
            if first:
                #one value is of the ckan archive is int while all other ar unicode...
                if isinstance(arr[key],unicode):
                    streams[normalize("NFKD", key).encode('ascii', 'ignore')] = [normalize("NFKD", arr[key]).encode('ascii', 'ignore')]
                else:
                    streams[normalize("NFKD", key).encode('ascii', 'ignore')] = [arr[key]]
            else:
                if isinstance(arr[key],unicode):
                    streams[normalize("NFKD", key).encode('ascii', 'ignore')].append([normalize("NFKD", arr[key]).encode('ascii', 'ignore')])
                else:
                    streams[normalize("NFKD", key).encode('ascii', 'ignore')].append(arr[key])
        first = False
    return streams

#msgType store, forward or transform
def wrapAndSendData(inp, msgType, connection, channelName):
    channel = connection.channel()
    channel.queue_declare(queue=channelName)
    timestamp = str(datetime.now())
    for arr in inp:
        data = {}
        data["type"] = msgType
        data["data"] = arr
        jsonData = json.dumps(data)
        channel.basic_publish(exchange='', routing_key='traffic', body=jsonData)

def main():
    connection = establishConnection()
    url = "http://ckan.projects.cavi.dk/api/action/datastore_search"
    resourceValues = "d7e6c54f-dc2a-4fae-9f2a-b036c804837d"
    resourceMetaData = "e132d528-a8a2-4e49-b828-f8f0bb687716"
    values = importData(url, resourceValues)
    trafficMetaData = importData(url, resourceMetaData)
    wrapAndSendData(trafficMetaData, 'store', connection, 'traffic')
    # for key in streams['data']:
    #     channel.basic_publish(exchange='', routing_key=key, body=streams[key])
    #     break

    connection.close()
    return

main()

# http://ckan.projects.cavi.dk/api/action/datastore_search?resource_id=d7e6c54f-dc2a-4fae-9f2a-b036c804837d&limit=5

# http://ckan.projects.cavi.dk/api/action/datastore_search?resource_id=e132d528-a8a2-4e49-b828-f8f0bb687716&limit=5

#
#
# def createStreamSensorCloud(streamId, data):
#     h = Http()
#     jsondump = json.dumps(data)
#     uri = "http://localhost:8000/streams/%s/data" %streamId
#     resp, content = h.request(uri, "POST", jsondump)
#     # assert resp.status == 200
#     pprint(content)
#     return resp.status == 200