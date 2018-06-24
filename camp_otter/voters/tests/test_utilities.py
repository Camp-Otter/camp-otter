from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from camp_otter.voters.utilities import import_voter_list_dataframe, import_uploaded_voter_file_to_db, \
    load_uploaded_file_to_dataframe, import_voter_history_dataframe
from camp_otter.core.models import Place, Person, Election
from camp_otter.voters.models import Voter

from camp_otter.voters.tests.testdata.dummy_data import UPLOADED_VOTER_LIST_CSV_DATA, UPLOADED_VOTER_HISTORY_CSV_DATA

import pandas as pd
import datetime


class VoterFileImportTests(TestCase):

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
        import_voter_list_dataframe(df)

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
        import_voter_list_dataframe(df)

        self.assertEqual(Place.objects.all().count(), 2)
        self.assertEqual(Person.objects.all().count(), 3)
        self.assertEqual(Voter.objects.all().count(), 3)
        self.assertEqual(str(Place.objects.last()), '200 Spring St, Newport, RI')
        self.assertEqual(str(Voter.objects.last().person.residence), '1 Broadway, Newport, RI')
        self.assertEqual(Voter.objects.first().voter_id, 10)

    def test_return_datafile_headers(self):
        file = SimpleUploadedFile('test.csv', UPLOADED_VOTER_LIST_CSV_DATA, content_type="text/csv")
        columns = load_uploaded_file_to_dataframe(file).columns
        self.assertEqual(columns[1], 'LAST NAME')

    def test_csv_file_import_to_df(self):
        data_dict = {
            'address': 'STREET NAME',
            'city': 'CITY',
            'state': 'STATE',
            'zip': 'ZIP CODE',
            'voter_id': 'VOTER ID',
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
        }
        file = SimpleUploadedFile('test.csv', UPLOADED_VOTER_LIST_CSV_DATA, content_type="text/csv")
        df = load_uploaded_file_to_dataframe(file, data_dict)
        import_voter_list_dataframe(df.dropna())
        self.assertEqual(Voter.objects.all().count(), 2)
        self.assertEqual(Place.objects.all().count(), 2)

    def test_xlsx_file_import_to_df(self):
        with open('camp_otter/voters/tests/testdata/dummy_data.xlsx') as infile:  #FIXME: Handle excel file with SimpleUploadedFile(). This works with manual testing
            file = SimpleUploadedFile('test.xlsx', infile.read())
            df = load_uploaded_file_to_dataframe(file)
            import_uploaded_voter_list_dataframe(df.dropna())
        self.assertEqual(Voter.objects.all().count(), 2)
        self.assertEqual(Place.objects.all().count(), 2)


class VoterHistoryImportTests(TestCase):

    def test_single_voter_history_write_from_df_to_empty_db(self):
        my_participation = {'date': ['2016-11-08'],
                            'election': ['GENERAL ELECTION'],
                            'voter_id': [100012],
                            'precinct': [2109],
                            }

        df = pd.DataFrame(my_participation)

        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', residence=house, voter_id=100012)
        voter.save()

        self.assertEqual(Voter.objects.all().count(), 1)  # just check to make sure voter hit the database
        self.assertEqual(Election.objects.all().count(), 0)

        import_voter_history_dataframe(df)  # import the history

        self.assertEqual(Election.objects.all().count(), 1)
        self.assertEqual(voter.voterparticipation_set.count(), 1)

    def test_multiple_voter_history_write_from_df_to_empty_db(self):
        my_participation = {'date': [datetime.datetime.strptime('2016-11-08', "%Y-%m-%d").date(),
                                     datetime.datetime.strptime('2016-06-01', "%Y-%m-%d").date()],
                            'election': ['GENERAL ELECTION', 'PRIMARY'],
                            'voter_id': [100012, 100012],
                            'precinct': [2109, 2109],
                            }

        df = pd.DataFrame(my_participation)

        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', residence=house, voter_id=100012)
        voter.save()

        self.assertEqual(Voter.objects.all().count(), 1)  # just check to make sure voter hit the database
        self.assertEqual(Election.objects.all().count(), 0)

        import_voter_history_dataframe(df)  # import the history

        self.assertEqual(Election.objects.all().count(), 2)
        self.assertEqual(voter.voterparticipation_set.count(), 2)

    def test_single_voter_history_write_from_df_with_existing_election(self):
        my_participation = {'date': ['2016-11-08'],
                            'election': ['GENERAL ELECTION'],
                            'voter_id': [100012],
                            'precinct': [2109],
                            }

        df = pd.DataFrame(my_participation)

        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', residence=house, voter_id=100012)
        voter.save()
        election = Election(election_date='2016-11-08', election_type='GENERAL ELECTION')
        election.save()

        self.assertEqual(Voter.objects.all().count(), 1)  # just check to make sure voter hit the database
        self.assertEqual(Election.objects.all().count(), 1)

        import_voter_history_dataframe(df)  # import the history

        self.assertEqual(Election.objects.all().count(), 1)
        self.assertEqual(voter.voterparticipation_set.count(), 1)

    def test_csv_history_file_import_to_df(self):
        history_data_dict = {
            'voter_id': 'VOTER ID',
            'date': 'DATE',
            'election': 'ELECTION',
            'precinct': 'PRECINCT',
        }
        voter_data_dict = {
            'address': 'STREET NAME',
            'city': 'CITY',
            'state': 'STATE',
            'zip': 'ZIP CODE',
            'voter_id': 'VOTER ID',
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
        }
        file = SimpleUploadedFile('test.csv', UPLOADED_VOTER_LIST_CSV_DATA, content_type="text/csv")
        df = load_uploaded_file_to_dataframe(file,voter_data_dict)
        import_voter_list_dataframe(df.dropna())
        file = SimpleUploadedFile('test.csv', UPLOADED_VOTER_HISTORY_CSV_DATA, content_type="text/csv")
        df = load_uploaded_file_to_dataframe(file, history_data_dict)
        import_voter_history_dataframe(df)
        self.assertEqual(Voter.objects.all().count(), 2)
        self.assertEqual(Place.objects.all().count(), 2)
        self.assertEqual(Voter.objects.get(voter_id=12).voterparticipation_set.count(), 1)
