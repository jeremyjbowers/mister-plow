#!/usr/bin/env python
from fabric.api import *

from dateutil.parser import *
import pymongo
import requests


def load_raw_data():
    """
    Script which loads DC snowplow data into a collection.
    """

    incidents_list = []

    r = requests.get('http://snowmap.dc.gov/getData.aspx?starttime=3/3/2013&endtime=3/6/2013&ne_lat=38.9845&ne_lng=-76.866&sw_lat=38.8012&sw_lng=-77.161')
    for row in r.content.split('||')[0].split('%%'):
        row_dict = {}
        cell = row.split(';;')
        row_dict['vehicle_id'] = cell[0]
        row_dict['lat'] = cell[1]
        row_dict['lng'] = cell[2]
        row_dict['time'] = parse(cell[3])
        row_dict['four'] = cell[4]
        row_dict['five'] = cell[5]
        incidents_list.append(row_dict)

    if len(incidents_list) > 0:
        connection = pymongo.MongoClient()
        db = connection.dcplow

        db.incidents.drop()

        incidents = db.incidents

        new_incidents = incidents.insert(incidents_list)

        print new_incidents
