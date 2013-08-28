from django.contrib import admin
from advertisements.models import Advertisement, Provider, Click
from django.db.models import Count


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('provider', 'ad_type', 'image', 'created', 'enabled', 'total_views')
    date_hierarchy = 'created'
    list_filter = ('ad_type', 'enabled', 'created')

    def total_views(self, obj):
        return obj.click_set.count()
    total_views.admin_order_field = 'clicks'

    def queryset(self, request):
        q = super(AdvertisementAdmin, self).queryset(request)
        q = q.annotate(clicks=Count('click'))
        return q

admin.site.register(Provider)
admin.site.register(Advertisement, AdvertisementAdmin)