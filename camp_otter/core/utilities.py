from camp_otter.core.models import Place

def create_places_from_dataframe(df):

    place_columns = ['street_number',
                     'street_name',
                     'street_address_2',
                     'unit',
                     'suffix_a',
                     'suffix_b',
                     'city',
                     'state',
                     'zip']  # specify the columns that correspond to place model

    place_df = df[[value for value in place_columns if value in df.columns]].drop_duplicates()

    place_object_list = []  # intialize empty list for bulk_write()

    # TODO: look into update_or_create methods to avoid duplication
    # if no places exist, start creating
    if not Place.objects.all():
        for row in place_df.iterrows():
            r = row[1]
            new_place = Place(
                    street_number=r.street_number,
                    street_name=r.street_name,
                    city=r.city,
                    state=r.state,
                    zip_code=r.zip
                )

            # handle optional fields
            if r.get('street_address_2'):
                new_place.street_address_2 = r.street_address_2
            if r.get('unit'):
                new_place.unit = r.unit
            if r.get('suffix_a'):
                new_place.suffix_a = r.suffix_a
            if r.get('suffix_b'):
                new_place.suffix_b = r.suffix_b

            place_object_list.extend([new_place])
        Place.objects.bulk_create(place_object_list)
    else:
        pass

    # check if places in state exist

    # then check if places in city exist

    # then check if places on street exist

    # then check if place at number exists

    # then check if unit exists

