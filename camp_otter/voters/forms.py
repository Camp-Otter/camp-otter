from django import forms


class UploadVoterFileForm(forms.Form):
    file = forms.FileField()

    # fields to define column headers containing required model data
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    voter_id = forms.CharField(max_length=50)
    address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip = forms.CharField(max_length=50)


class UploadHistoryFileForm(forms.Form):
    file = forms.FileField()

    # fields to define column headers containing required model data
    voter_id = forms.CharField(max_length=50)
    election_date = forms.CharField(max_length=50)
    election_type = forms.CharField(max_length=50)
    voter_precinct = forms.CharField(max_length=50)