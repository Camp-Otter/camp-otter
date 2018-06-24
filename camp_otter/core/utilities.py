from camp_otter.core.models import Place

def create_places_from_dataframe(df):

    place_columns = ['address', 'city', 'state', 'zip']  # specify the columns that correspond to place model

    place_df = df[place_columns].drop_duplicates()

    place_object_list = []  # intialize empty list for bulk_write()

    # TODO: look into update_or_create methods to avoid duplication
    # if no places exist, start creating
    if not Place.objects.all():
        for row in place_df.iterrows():
            r = row[1]
            place_object_list.extend([
                Place(
                    street_address=r.address,
                    city=r.city,
                    state=r.state,
                    zip_code=r.zip
                )
            ])
        Place.objects.bulk_create(place_object_list)
    else:
        pass

    # check if places in state exist

    # then check if places in city exist

    # then check if places on street exist

    # then check if place at number exists

    # then check if unit exists

