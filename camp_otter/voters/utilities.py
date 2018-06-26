from camp_otter.core.models import Person, Place, Election
from camp_otter.voters.models import Voter

import pandas as pd

from camp_otter.core.utilities import create_places_from_dataframe


def import_voter_list_dataframe(df):
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
        voter_residence = Place.objects.filter(street_number=r.street_number, street_name=r.street_name, city=r.city, state=r.state, zip_code=r.zip).first()  # this should return only one result
        person_list.extend([Person(first_name=r.first_name, last_name=r.last_name, residence=voter_residence, date_of_birth=r.date_of_birth)])
        voter_id_list.extend([r.voter_id])

    Person.objects.bulk_create(person_list)

    voters = tuple(zip(person_list, voter_id_list))

    voter_list = []
    for p, i in voters:
        voter_list.extend([Voter(person=p, voter_id=i)])
    Voter.objects.bulk_create(voter_list)


def import_voter_history_dataframe(df):

    # The voter history dataframe needs to be structured as a list of individual voter participation actions

    # get all elections currently in the database
    election_queryset = Election.objects.all()

    # get unique elections in the dataframe and create them in the database if they're not there already
    elections_in_history = df.drop_duplicates(['date', 'election'])
    voters_in_history = df.voter_id.unique()

    new_election_objects_list = []  # empty list to keep elections to be created
    existing_election_objects_list = []
    new_election_dates_list = []  # list of new election dates for keeping track
    existing_election_dates_list = []

    for elec in elections_in_history.iterrows():
        e = elec[1]
        if not election_queryset.filter(election_date=str(e.date), election_description=e.election_description).exists():
            new_election_objects_list.extend([Election(election_date=str(e.date), election_description=e.election_description)])
            new_election_dates_list.extend([str(e.date)])

    Election.objects.bulk_create(new_election_objects_list)

    election_dict = dict(zip(new_election_dates_list, new_election_objects_list))

    for q in election_queryset:
        election_dict[str(q.election_date)] = q  # use string of datetime.date object

    # iterate through voters in the history dataframe
    for v in voters_in_history:
        voter_history_df = df[df['voter_id'] == v]
        this_voter = Voter.objects.get(voter_id__exact=v)

        if not this_voter.voterparticipation_set.exists():  # if no voter history is present in database, add everything
            for row in voter_history_df.iterrows():
                r = row[1]
                this_voter.add_election(election=election_dict[str(r.date)], precinct=r.precinct)

        else:  # check voterparticipation_set for existing event matching this one, and create new if doesn't exist
            for row in voter_history_df.iterrows():
                r = row[1]
                if not this_voter.voterparticipation_set.filter(election__election_date=str(r.date)).exists():
                    this_voter.add_election(election=election_dict[str(r.date)], precinct=r.precinct)


def load_uploaded_file_to_dataframe(file, field_dict=None):
    """
    A utility function to read structured tabular data from an uploaded file and determine the input for pandas
    :param file: a csv or Excel file with the data
            field_dict: a dictionary mapping model data to column names.  uses the file headers by default
    :return: pandas.DataFrame() object
    """

    filename = file.name
    if filename.endswith('.csv'):
        df = pd.read_csv(file, header=0)
    elif filename.endswith('.xls') or filename.endswith('.xlsx'):
        df = pd.read_excel(file, header=0)

    # if field mapping isn't specified, assume the column headers are already mapped
    if field_dict is not None:
        filtered_data = df[list(field_dict.values())]
        filtered_data.columns = list(field_dict.keys())
    else:
        filtered_data = df

    return filtered_data


def import_uploaded_voter_file_to_db(df):

    import_voter_list_dataframe(df.dropna())
