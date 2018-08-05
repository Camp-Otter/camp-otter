from django.test import TestCase
from django.db import connections
from camp_otter.core.utilities import create_places_from_dataframe
from camp_otter.core.postgis_utilities import tiger_geocode_address
from camp_otter.core.models import Place

import pandas as pd

class TestPlacesUtilities(TestCase):

    def test_create_places_from_dataframe_in_empty_db(self):
        # define test dataframe with repeated places

        data = {
                'street_number': ['1', '1', '200'],
                'street_name': ['Broadway', 'Broadway', 'Spring St'],
                'city': ['Newport', 'Newport', 'Newport'],
                'state': ['RI', 'RI', 'RI'],
                'zip': ['02840', '02840', '02840'],
                }

        df = pd.DataFrame(data)
        create_places_from_dataframe(df)
        self.assertEqual(Place.objects.all().count(), 2)

    def test_tiger_geocoding(self):
        # FIXME: it seems like this test fails because of something with the test database - it works in the console
        address = "43 Broadway, Newport, RI, 02840"
        geo = tiger_geocode_address('tiger', address)
        self.assertEqual(geo[2], 41.4918411453327)
