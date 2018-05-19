from django.contrib import admin
from camp_otter.core.models import Place, Person, Election

# Register your models here.
admin.site.register(Place)
admin.site.register(Person)
admin.site.register(Election)
