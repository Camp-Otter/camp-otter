from django import forms


class UploadVoterFileForm(forms.Form):
    file = forms.FileField()

    # fields to define column headers containing required model data
    first_name = forms.CharField()
    last_name = forms.CharField()
    voter_id = forms.CharField()
    street_number = forms.CharField()
    street_name = forms.CharField()
    street_name_2 = forms.CharField()
    unit = forms.CharField()
    suffix_a = forms.CharField()
    suffix_b = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zip = forms.CharField()


class UploadHistoryFileForm(forms.Form):
    file = forms.FileField()

    # fields to define column headers containing required model data
    voter_id = forms.CharField()
    election_date = forms.CharField()
    election_type = forms.CharField()
    voter_precinct = forms.CharField()
