import csv
from globemaster.location import Location


def read_contents(file) -> [Location]:
    """Reads a CSV file of 'lat, long' coordinates """
    with open(file) as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        return [Location(id, name, float(lat), float(long)) for id, name, lat, long in reader]


# Tests
if __name__ == '__main__':
    print(read_contents('../database/test_coordinates.csv'))
