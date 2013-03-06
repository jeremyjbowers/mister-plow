#!/usr/bin/env python
import json
import time
from sets import Set

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
        item_dict['detail_uri'] = '/plow/vehicles/%s/' % item_dict['vehicle_id']
        incident_list.append(item_dict)
    return incident_list, len(incident_list)


@app.route('/plow/', methods=['GET'])
def incident_list():
    """
    Returns a list of incidents in JSON.
    """

    # Connect.
    connection = pymongo.MongoClient()
    db = connection.dcplow

    # Get everything in the DB.
    query = db.incidents.find()
    query = prep_incidents(query)

    # Prepare a response.
    response = {}
    response['incidents'] = {}
    response['incidents']['items'] = sorted(query[0], key=lambda item: item['time'], reverse=True)
    response['incidents']['count'] = query[1]

    # Return the response.
    return json.dumps(response)


@app.route('/plow/vehicles/', methods=['GET'])
def incidents_grouped_by_vehicle():
    """
    Returns all incidents, grouped by vehicle ID.
    """

    # Connect.
    connection = pymongo.MongoClient()
    db = connection.dcplow

    # Get the incidents for this vehicle_id.
    query = db.incidents.find()

    vehicles_dict = {}
    count = 0
    vehicles = Set([])
    for item in query:
        item_dict = {}
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item_dict['object_id'] = value.__str__()
            elif key == 'time':
                item_dict['time'] = time.mktime(value.timetuple())
                item_dict['time_string'] = value.strftime('%m/%d/%Y %H:%M:%S %p')
            else:
                item_dict[key] = value
        item_dict['detail_uri'] = '/plow/vehicles/%s/' % item_dict['vehicle_id']
        vehicles_dict.setdefault(item_dict['vehicle_id'], []).append(item_dict)
        count += 1

        for item in vehicles_dict:
            vehicles.add(item)

    # Prepare the response.
    response = {}
    response['incidents'] = {}
    response['vehicles'] = {}
    response['incidents']['items'] = vehicles_dict
    response['incidents']['count'] = count
    response['vehicles']['count'] = len(vehicles)
    response['vehicles']['items'] = list(vehicles)

    # Return the response.
    return json.dumps(response)


@app.route('/plow/vehicles/<vehicle_id>/', methods=['GET'])
def incidents_by_vehicle(vehicle_id):
    """
    Returns a list of incidents for each vehicle ID.
    """

    # Connect.
    connection = pymongo.MongoClient()
    db = connection.dcplow

    # Get the incidents for this vehicle_id.
    query = db.incidents.find({'vehicle_id': vehicle_id})
    query = prep_incidents(query)

    # Prepare the response.
    response = {}
    response['incidents'] = {}
    response['incidents']['items'] = sorted(query[0], key=lambda item: item['time'], reverse=True)
    response['incidents']['count'] = query[1]

    # Return the response.
    return json.dumps(response)

# Give Flask wings.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
