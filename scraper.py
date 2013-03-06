#!/usr/bin/env python
from dateutil.parser import *
import pymongo
import requests

incidents_list = []

# Scrape this URL.
# Bounding box from @stiles.
r = requests.get('http://snowmap.dc.gov/getData.aspx?starttime=3/3/2013&endtime=3/6/2013&ne_lat=38.9845&ne_lng=-76.866&sw_lat=38.8012&sw_lng=-77.161')

# First, remove the gross stuff at the bottom of the response.
# Then, split on the actual delimiter, which is %%.
for row in r.content.split('||')[0].split('%%'):

    # Set up storage for this row.
    row_dict = {}

    # Cells are delimited with ;;.
    cell = row.split(';;')

    # Update the row_dict with our data.
    row_dict['vehicle_id'] = cell[0]
    row_dict['lat'] = cell[1]
    row_dict['lng'] = cell[2]
    row_dict['time'] = parse(cell[3])

    # No idea what these are.
    row_dict['four'] = cell[4]
    row_dict['five'] = cell[5]

    # Append the dictionary.
    incidents_list.append(row_dict)

# Make sure there are some incidents before inserting.
# The site goes down all the time.
if len(incidents_list) > 0:

    # Connect to our mongod instance.
    connection = pymongo.MongoClient()
    db = connection.dcplow

    # Drop the old incidents.
    db.incidents.drop()

    # Create the collection.
    incidents = db.incidents

    # Bulk insert the new incidents
    new_incidents = incidents.insert(incidents_list)
