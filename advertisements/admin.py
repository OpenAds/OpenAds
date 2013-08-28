from django.contrib import admin
from advertisements.models import Advertisement, Provider


admin.site.register(Provider)
admin.site.register(Advertisement)