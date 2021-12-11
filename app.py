import sqlite3
from flask import Flask, render_template, g, url_for, request
from werkzeug.exceptions import abort

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
    cur = db.execute(command, args)
    db.commit()


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


def get_post(post_id):
    post = query_db('SELECT * FROM posts WHERE id = ?', (post_id,))
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    posts = query_db('SELECT * FROM posts')
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/api/getLocations', methods=['GET'])
def get_locations():
    """This method currently takes 3 URL parameters and just returns them in a JSON response"""
    x = request.args.get('x', 0)
    y = request.args.get('y', 0)
    distance = request.args.get('distance', 100)

    return {
        "userProps": {
            "lat": x,
            "long": y,
            "distance": distance
        },
        "locations": [
            {
                "lat": x,
                "long": y,
                "distance": distance
            }
        ]
    }


with app.test_request_context():
    print(url_for('index'))
    print(url_for('post', post_id=5))
    print(url_for('get_locations'))

