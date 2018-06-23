from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

    # fields to define column headers containing required model data
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    voter_id = forms.CharField(max_length=50)
    address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip = forms.CharField(max_length=50)


