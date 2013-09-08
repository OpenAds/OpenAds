from django.contrib import admin
from advertisements.models import Advertisement, Provider, Click
from django.db.models import Count


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('provider', 'ad_type', 'image_thumbnail', 'created', 'status', 'total_clicks')
    date_hierarchy = 'created'
    list_filter = ('ad_type', 'status', 'created')

    def total_clicks(self, obj):
        return obj.click_set.count()
    total_clicks.admin_order_field = 'clicks'

    def image_thumbnail(self, obj):

        width = 125
        if obj.ad_type == Advertisement.TOP_AD:
            width = 300

        return '<img src="{0}" width="{1}" />'.format(obj.image.url, width)
    image_thumbnail.allow_tags = True

    def queryset(self, request):
        q = super(AdvertisementAdmin, self).queryset(request)
        q = q.annotate(clicks=Count('click'))
        return q

    def make_enabled(self, request, queryset):
        updated_count = queryset.update(status=Advertisement.ACTIVE)
        if updated_count == 1:
            message_beginning = '1 advertisement was'
        else:
            message_beginning = '{0} advertisements were'.format(updated_count)
        self.message_user(request, "{0} successfully enabled.".format(message_beginning))

    make_enabled.short_description = 'Enable the selected advertisements'

    def make_disabled(self, request, queryset):
        updated_count = queryset.update(status=Advertisement.INACTIVE)
        if updated_count == 1:
            message_beginning = '1 advertisement was'
        else:
            message_beginning = '{0} advertisements were'.format(updated_count)
        self.message_user(request, "{0} successfully disabled.".format(message_beginning))

    make_disabled.short_description = 'Disable the selected advertisements'

    actions = [make_enabled, make_disabled]

admin.site.register(Provider)
admin.site.register(Advertisement, AdvertisementAdmin)