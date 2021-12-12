import sqlite3
from flask import Flask, render_template, g, url_for, request, redirect, abort

from globemaster.location import Location

# Sqlite dev database file.
DATABASE = 'database/database.db'

# Start the Flask web server
app = Flask(__name__)


def get_db():
    """Attach SQLite connection to the global application context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    """
    Simplifies dealing with the raw Cursor objects by just returning the Row object directly.
    If a query specifies the 'one' flag as True, just return the first item in the cursor fetch.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(command, args=()):
    db = get_db()
    output = db.execute(command, args)
    id = output.lastrowid
    db.commit()
    return id


def get_location_from_db(location_id: int):
    item = query_db("SELECT * FROM locations WHERE id = ?", (location_id,), one=True)
    loc = Location(item['id'], item['name'], item['latitude'], item['longitude'])
    return loc


def get_all_locations_from_db(limit=10):
    return query_db("SELECT * FROM locations LIMIT ?", (limit,))


def insert_location_db(name: str, latitude: float, longitude: float):
    return insert_db("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)",
                     (name, latitude, longitude)
                     )


@app.teardown_appcontext
def close_connection(exception):
    """Close SQL connection after tearing down the application context."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def index():
    locations = get_all_locations_from_db()
    return render_template('index.html', locations=locations)


@app.route('/location/<int:location_id>')
def location(location_id):
    item = get_location_from_db(location_id)
    return render_template('location.html', location=item)


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """This method currently takes 3 URL parameters and just returns them in a JSON response"""
    lat = request.args.get('lat', 0)
    long = request.args.get('long', 0)
    radius = request.args.get('radius', 100)
    locations = get_all_locations_from_db()

    return {
        "userProps": {
            "lat": lat,
            "long": long,
            "radius": radius
        },
        "locations": locations
    }


@app.route('/api/locations', methods=['POST'])
def create_location():
    if not request.is_json:
        return abort(404)
    r = request.json

    name, latitude, longitude = r['name'], r['latitude'], r['longitude']
    new_id = insert_location_db(name, latitude, longitude)

    return redirect(url_for('location', location_id=new_id))

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('post', post_id=5))
#     print(url_for('get_locations'))
