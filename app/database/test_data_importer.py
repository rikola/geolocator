import csv

# Test file contains all cities over 5000 population with the following TSV schema from https://download.geonames.org/export/dump/:
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
# admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
# admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int)
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
# timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format
from app.model.location import Location

TEST_COORDINATES_FILE = "../../data/test_coordinates.csv"
GEONAMES_FILE = "../../data/cities5000.tsv"


def read_geonames_file(file=GEONAMES_FILE):
    with open(file) as tsv_file:
        reader = csv.reader(tsv_file, delimiter="\t")
        results = []
        for line in reader:
            results.append((line[1], line[4], line[5]))

        return results


def read_contents(file=TEST_COORDINATES_FILE) -> [Location]:
    """Reads a CSV file of 'lat, long' coordinates """
    with open(file) as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        return [Location(id, name, float(lat), float(long)) for id, name, lat, long in reader]


# Tests
if __name__ == '__main__':
    # print(read_contents('../database/test_coordinates.csv'))
    print(read_geonames_file(GEONAMES_FILE))
