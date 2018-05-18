from camp_otter.core.models import Person, Place
from camp_otter.voters.models import Voter

from camp_otter.core.utilities import create_places_from_dataframe


def import_voter_dataframe(df):
    """
    :param df:
    :return:
    """
    num_records = len(df)  # number of records in the dataframe

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
