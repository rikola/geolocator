import csv
from location import Location


def read_contents(file) -> [Location]:
    """Reads a CSV file of 'lat, long' coordinates """
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        return [Location(name, float(lat), float(long)) for name, lat, long in reader]


# Tests
print(read_contents('../database/test_coordinates.csv'))
