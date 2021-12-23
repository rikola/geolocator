import os.path
import sqlite3

from app.database import test_data_importer
from app.utils import get_data_path

if __name__ == "__main__":
    path = get_data_path()
    file = os.path.join(path, "database.db")
    connection = sqlite3.connect(file)

    connection.execute("DROP TABLE IF EXISTS locations")
    # Create the table
    with open('schema.sql') as f:
        connection.executescript(f.read())

    # Read test data from file.
    # locations = test_data_importer.read_contents(COORDINATE_FILE)
    locations = test_data_importer.read_geonames_file()

    # Insert test data into table.
    cur = connection.cursor()
    for loc in locations:
        cur.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)",
                    (loc[0], loc[1], loc[2])
                    )

    connection.commit()
    connection.close()
