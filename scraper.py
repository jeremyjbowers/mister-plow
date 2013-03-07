#!/usr/bin/env python
import datetime
from datetime import timedelta

from dateutil.parser import *
import pymongo
import requests

incidents_list = []

# Bounding box from @stiles. For all of the DC metro area.
box = '&ne_lat=38.9845&ne_lng=-76.866&sw_lat=38.8012&sw_lng=-77.161'

# Construct a start and end time. Only scrape a few days (they're SLOOOOOOOOW).
end_time = datetime.date.today().strftime('%m/%d/%Y')
start_time = (datetime.date.today() - timedelta(3)).strftime('%m/%d/%Y')

# Construct the URL.
url = 'http://snowmap.dc.gov/getData.aspx?starttime=%s&endtime=%s%s' % (start_time, end_time, box)

# Scrape this URL.
r = requests.get(url)

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
