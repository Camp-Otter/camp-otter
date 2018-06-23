from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from camp_otter.voters.utilities import import_voter_dataframe, import_uploaded_voter_file_to_db, load_uploaded_file_to_dataframe
from camp_otter.core.models import Place, Person
from camp_otter.voters.models import Voter

from camp_otter.voters.tests.testdata.dummy_data import UPLOADED_CSV_DATA

import pandas as pd


class FileImportTests(TestCase):

    def test_voter_dataframe_write_to_db(self):

        # define the dummy voter data
        my_voter = {'voter_id': [10],
                    'first_name': ['Joe'],
                    'last_name': ['Test'],
                    'address': ['1 Broadway'],
                    'city': ['Newport'],
                    'state': ['RI'],
                    'zip': ['02840']}

        df = pd.DataFrame(my_voter)
        import_voter_dataframe(df)

        # the size of the place, person, and voter tables should be 1
        self.assertEqual(Place.objects.all().count(), 1)
        self.assertEqual(Person.objects.all().count(), 1)
        self.assertEqual(Voter.objects.all().count(), 1)

    def test_add_multiple_voters_in_dataframe(self):
        my_voters = {'voter_id': [10, 11, 12],
                     'first_name': ['Joe', 'Steve', 'John'],
                     'last_name': ['Test', 'Bones', 'Doe'],
                     'address': ['1 Broadway', '200 Spring St', '1 Broadway'],
                     'city': ['Newport', 'Newport', 'Newport'],
                     'state': ['RI', 'RI', 'RI'],
                     'zip': ['02840', '02840', '02840']}

        df = pd.DataFrame(my_voters)
        import_voter_dataframe(df)

        self.assertEqual(Place.objects.all().count(), 2)
        self.assertEqual(Person.objects.all().count(), 3)
        self.assertEqual(Voter.objects.all().count(), 3)
        self.assertEqual(str(Place.objects.last()), '200 Spring St, Newport, RI')
        self.assertEqual(str(Voter.objects.last().person.residence), '1 Broadway, Newport, RI')
        self.assertEqual(Voter.objects.first().voter_id, 10)

    def test_return_datafile_headers(self):
        file = SimpleUploadedFile('test.csv', UPLOADED_CSV_DATA, content_type="text/csv")
        columns = load_uploaded_file_to_dataframe(file).columns
        self.assertEqual(columns[1], 'LAST NAME')

    def test_csv_file_import_to_df(self):
        file = SimpleUploadedFile('test.csv', UPLOADED_CSV_DATA, content_type="text/csv")
        df = load_uploaded_file_to_dataframe(file)
        import_uploaded_voter_file_to_db(df)
        # this should print out a dataframe in the console
        self.assertEqual(Voter.objects.all().count(), 2)
        self.assertEqual(Place.objects.all().count(), 2)

    def test_xlsx_file_import_to_df(self):
        with open('camp_otter/voters/tests/testdata/dummy_data.xlsx') as infile:  #FIXME: Handle excel file with SimpleUploadedFile(). This works with manual testing
            file = SimpleUploadedFile('test.xlsx', infile.read())
            df = load_uploaded_file_to_dataframe(file)
            import_uploaded_voter_file_to_db(df)
            # this should print out a dataframe in the console
        self.assertEqual(Voter.objects.all().count(), 2)
        self.assertEqual(Place.objects.all().count(), 2)
