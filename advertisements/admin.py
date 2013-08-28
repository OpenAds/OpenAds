from django.contrib import admin
from advertisements.models import Advertisement, Provider


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('provider', 'ad_type', 'image', 'created')
    date_hierarchy = 'created'
    list_filter = ('ad_type', 'created')


admin.site.register(Provider)
admin.site.register(Advertisement, AdvertisementAdmin)