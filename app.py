#!/usr/bin/env python
import json
import time

from bson.objectid import ObjectId
from flask import Flask
import pymongo

app = Flask(__name__)


def prep_incidents(incidents):
    """
    Prepares an incident list to be JSON stringified.
    """
    incident_list = []
    for item in incidents:
        item_dict = {}
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item_dict['object_id'] = value.__str__()
            elif key == 'time':
                item_dict['time'] = time.mktime(value.timetuple())
                item_dict['time_string'] = value.strftime('%m/%d/%Y %H:%M:%S %p')
            else:
                item_dict[key] = value
        incident_list.append(item_dict)
    return incident_list, len(incident_list)


@app.route('/plow/', methods=['GET'])
def incident_list():
    connection = pymongo.MongoClient()
    db = connection.dcplow
    query = db.incidents.find()
    query = prep_incidents(query)
    response = {}
    response['items'] = sorted(query[0], key=lambda item: item['time'], reverse=True)
    response['count'] = query[1]
    return json.dumps(response)


@app.route('/plow/vehicle/<vehicle_id>/', methods=['GET'])
def vehicle_list(vehicle_id):
    connection = pymongo.MongoClient()
    db = connection.dcplow
    query = db.incidents.find({'vehicle_id': vehicle_id})
    query = prep_incidents(query)
    response = {}
    response['items'] = sorted(query[0], key=lambda item: item['time'], reverse=True)
    response['count'] = query[1]
    return json.dumps(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
