from django.views.generic.list import ListView
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from camp_otter.voters.models import Voter
from camp_otter.voters.forms import UploadFileForm
from camp_otter.voters.utilities import import_uploaded_voter_file_to_db, load_uploaded_file_to_dataframe


# Create your views here.
def success(request):
    return render(request, 'voters/success.html')


class VoterListView(ListView):
    model = Voter
    paginate_by = 1  # the number of voters shown per page
    template_name = 'voters/voter_list.html'

    def get_queryset(self):
        return Voter.objects.order_by('person__last_name', 'person__first_name')


# Upload view based on https://www.andygoldschmidt.com/2014/09/10/django-file-uploads-with-class-based-views/
class FileUploadView(View):
    form_class = UploadFileForm
    success_url = reverse_lazy('success')
    template_name = 'voters/file_upload.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # TODO: render a table with a preview of the uploaded file to allow selection of columns
            # build data dictionary from form input

            data_dict = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'voter_id': form.cleaned_data['voter_id'],
                        'address': form.cleaned_data['address'],
                        'city': form.cleaned_data['city'],
                        'state': form.cleaned_data['state'],
                        'zip': form.cleaned_data['zip'],
                        }
            df = load_uploaded_file_to_dataframe(request.FILES['file'])
            import_uploaded_voter_file_to_db(df, data_dict)
            return redirect(self.success_url)  # TODO: render file in preprocessing view
        else:
            return render(request, self.template_name, {'form': form})
