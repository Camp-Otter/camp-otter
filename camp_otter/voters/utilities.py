from camp_otter.core.models import Person, Place
from camp_otter.voters.models import Voter

import pandas as pd

from camp_otter.core.utilities import create_places_from_dataframe


def import_voter_dataframe(df):
    """
    :param df:
    :return:
    """

    # create places by getting unique addresses
    create_places_from_dataframe(df)
    person_list = []
    voter_id_list = []

    for row in df.iterrows():
        r = row[1]
        voter_residence = Place.objects.filter(street_address=r.address, city=r.city, state=r.state, zip_code=r.zip).first()  # this should return only one result
        person_list.extend([Person(first_name=r.first_name, last_name=r.last_name, residence=voter_residence)])
        voter_id_list.extend([r.voter_id])

    Person.objects.bulk_create(person_list)

    voters = tuple(zip(person_list, voter_id_list))

    voter_list = []
    for p, i in voters:
        voter_list.extend([Voter(person=p, voter_id=i)])
    Voter.objects.bulk_create(voter_list)


def handle_uploaded_voter_file(file):

    # read file into a dataframe
    filename = file.name
    if filename.endswith('.csv'):
        df = pd.read_csv(file, header=0)
    elif (filename.endswith('.xls') or filename.endswith('.xlsx')):
        df = pd.read_excel(file, header=0)


    # dictionary to translate file columns to model fields
    field_dict = {
        'first_name': 'FIRST NAME',
        'last_name': 'LAST NAME',
        'voter_id': 'VOTER ID',
        'address': 'STREET NAME',
        'city': 'CITY',
        'state': 'STATE',
        'zip': 'ZIP CODE',
    }

    filtered_data = df[list(field_dict.values())]
    filtered_data.columns = list(field_dict.keys())

    print(filtered_data.head())

    import_voter_dataframe(filtered_data.dropna())
