from django.db import connections


def tiger_geocode_address(database, address):
    # run postgis commands to use the tiger geocoder
    with connections[database].cursor() as cursor:
        # TODO: check to make sure this doesn't create a SQL injection vulnerability
        # TODO: select appropriate fields for output
        cursor.execute("SELECT g.rating, ST_X(g.geomout) As lon, ST_Y(g.geomout) As lat, (addy).address As stno, (addy).streetname As street, (addy).streettypeabbrev As styp, (addy).location As city, (addy).stateabbrev As st, (addy).zip FROM geocode( %s ) As g;", [address])
        row = cursor.fetchone()
        return row

def pretty_address(database, address):
    # https: // postgis.net / docs / Pprint_Addy.html
    with connections[database].cursor() as cursor:
        # TODO: check to make sure this doesn't create a SQL injection vulnerability
        cursor.execute("SELECT pprint_addy(normalize_address(%s)) As pretty_address;", [address])
        row = cursor.fetchone()
        return row[0]