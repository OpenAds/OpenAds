from django.contrib import admin
from advertisements.models import Advertisement, Provider, Click
from django.db.models import Count


def make_enabled(modeladmin, request, queryset):
    # This is the only safe way to update due to the annotate below
    for advert in queryset:
        advert.enabled = True
        advert.save()
make_enabled.short_description = 'Enable the selected advertisements'


def make_disabled(modeladmin, request, queryset):
    # This is the only safe way to update due to the annotate below
    for advert in queryset:
        advert.enabled = False
        advert.save()
make_disabled.short_description = 'Disable the selected advertisements'


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('provider', 'ad_type', 'image', 'created', 'enabled', 'total_views')
    date_hierarchy = 'created'
    list_filter = ('ad_type', 'enabled', 'created')
    actions = [make_enabled, make_disabled]

    def total_views(self, obj):
        return obj.click_set.count()
    total_views.admin_order_field = 'clicks'

    def queryset(self, request):
        q = super(AdvertisementAdmin, self).queryset(request)
        q = q.annotate(clicks=Count('click'))
        return q

admin.site.register(Provider)
admin.site.register(Advertisement, AdvertisementAdmin)