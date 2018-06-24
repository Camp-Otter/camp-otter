from django.test import TestCase
from camp_otter.core.utilities import create_places_from_dataframe
from camp_otter.core.models import Place

import pandas as pd

class TestPlacesUtilities(TestCase):

    def test_create_places_from_dataframe_in_empty_db(self):
        # define test dataframe with repeated places

        data = {'address': ['1 Broadway', '1 Broadway', '200 Spring St'],
                'city': ['Newport', 'Newport', 'Newport'],
                'state': ['RI', 'RI', 'RI'],
                'zip': ['02840', '02840', '02840'],
                }

        df = pd.DataFrame(data)
        create_places_from_dataframe(df)
        self.assertEqual(Place.objects.all().count(), 2)
