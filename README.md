# geolocator
A demonstration of a quad-tree based geo-spacial search website. (Similar to Google Maps!)

This is a Python and Flask based Web App for the time being. Will be expanding out to include a better browsing website.

## Quickstart
1. You will need `Pipenv` installed. Run `pipenv install` at the project root.
2. To initialize the SQLite database the first time, run the `database/init_db.py` script.
3. Start the web server with: `flask run`

## Notes
To perform POST requests to the Locations API routes, you need to use CURL.  
Example which creates a new location:
```commandline
curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Sesame Street", "latitude": -72.123456, "longitude": 32.123987}' http://localhost:5000/api/locations
```

## Troubleshooting
* If you are having issues with the SQLite local database, just delete the `database/database.db` file and 
  re-run the `database/init_db.py` script to re-create it.