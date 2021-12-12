import sqlite3

from database import coordinate_importer

COORDINATE_FILE = 'test_coordinates.csv'

connection = sqlite3.connect('database.db')

# Create the table
with open('schema.sql') as f:
    connection.executescript(f.read())

# Read test data from CSV file.
locations = coordinate_importer.read_contents(COORDINATE_FILE)

# Insert test data into table.
cur = connection.cursor()
for loc in locations:
    cur.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)",
                (loc.name, loc.latitude, loc.longitude)
                )

connection.commit()
connection.close()
