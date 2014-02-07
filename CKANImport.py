__author__ = 'Daniel'
import urllib2
import urllib
import json
from pprint import pprint
from httplib2 import Http
from unicodedata import normalize
from datetime import datetime

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
                streams[normalize("NFKD", key).encode('ascii', 'ignore')] = [arr[key]]
            else:
                streams[normalize("NFKD", key).encode('ascii', 'ignore')].append(arr[key])
        first = False
    return streams

def wrapData(inp):
    timestamp = str(datetime.now())
    data = {}
    data["data"] = []
    for v in inp:
        d = {"timestamp": timestamp, "value": v}
        data["data"].append(d)
    return data


def createStream(streamId, data):
    h = Http()
    jsondump = json.dumps(data)
    uri = "http://localhost:8000/streams/%s/data" %streamId
    resp, content = h.request(uri, "POST", jsondump)


def main():
    url = "http://ckan.projects.cavi.dk/api/action/datastore_search"
    resourceValues = "d7e6c54f-dc2a-4fae-9f2a-b036c804837d"
    resourceMetaData = "e132d528-a8a2-4e49-b828-f8f0bb687716"
    values = importData(url, resourceValues)
    metaData = importData(url, resourceMetaData)
    streams = splitInStreams(metaData)
    # pprint(streams)
    for key in streams:
        wrappedData = wrapData(streams[key])
        createStream(key, wrappedData)

main()

# http://ckan.projects.cavi.dk/api/action/datastore_search?resource_id=d7e6c54f-dc2a-4fae-9f2a-b036c804837d&limit=5

# http://ckan.projects.cavi.dk/api/action/datastore_search?resource_id=e132d528-a8a2-4e49-b828-f8f0bb687716&limit=5
