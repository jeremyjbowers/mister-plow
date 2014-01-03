# Mister Plow

Mister Plow is:

* A scraper for the DC City snowplow location data.
* A lightweight Flask app for returning JSON.

Either of these things might be useful to you.

## See it in action!
* Map via [@vtcraghead](http://twitter.com/@vtcraghead): [http://dev.geosprocket.com/mapbox/dcplows/](http://dev.geosprocket.com/mapbox/dcplows/)
* API: [http://www.jeremybowers.com/plow/vehicles/](http://www.jeremybowers.com/plow/vehicles/)

## Setup

1. Install mongodb.
2. Run mongodb locally.
3. Create a virtualenv for this project.
4. ```pip install -r requirements.txt```
5. ```./scraper.py```

## JSON

* ```/plow/```: Returns a list of snowplow incidents, sorted newest-to-oldest.
* ```/plow/vehicles/```: Returns a list of vehicles, with a list of snowplow incidents per vehicle, sorted newest-to-oldest.
* ```/plow/vehicle/<vehicle_id>```: Returns a list of snowplow incidents for a single vehicle, sorted newest-to-oldest.

## Cron

Run the cron every five minutes as the ubuntu user. Note: This user is not required, just an example.

```*/5 * * * * ubuntu /usr/local/bin/virtualenvwrapper.sh && workon mister-plow && /home/ubuntu/apps/mister-plow/repository/scraper.py```
