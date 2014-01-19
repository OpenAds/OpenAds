from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template import Context, Template
from advertisements.models import Advertisement, Provider, Click, AdvertisementPanel
from django.db.models import Count


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('provider', 'panel', 'image_thumbnail', 'created', 'status', 'total_clicks')
    date_hierarchy = 'created'
    list_filter = ('panel', 'status', 'created')

    def total_clicks(self, obj):
        return obj.click_set.count()
    total_clicks.admin_order_field = 'clicks'

    def image_thumbnail(self, obj):

        return '<img src="{0}" width="{1}" height="{2}" />'.format(obj.image.url, obj.panel.width, obj.panel.height)
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


class PanelAdmin(admin.ModelAdmin):
    readonly_fields = ('look_and_feel', 'embed_url',)
    list_display = ('name', 'width', 'height', 'cols', 'rows',)

    def look_and_feel(self, instance):
        if instance.pk is None:
            return "Preview available after save"
        return Template("""
        {% spaceless %}
        <iframe src="{% url 'advert:preview_size' panel.width panel.height panel.cols panel.rows %}" height={{ panel.total_height }} width={{ panel.total_width }} style="border: none;">
        </iframe>
        {% endspaceless %}
        """).render(Context({
            "panel": instance,
        }))

    look_and_feel.allow_tags = True
    look_and_feel.short_description = 'Preview'

    def embed_url(self, instance):
        if instance.pk is None:
            return "Embed URL available after save"

        return format_html(
            "{0} {1}",
            instance.get_iframe_url(),
            mark_safe("<br> <strong>Replace [INSERT_BASE_URL_HERE] with the site url</strong>")
        )
    embed_url.allow_tags = True
    embed_url.short_description = "Embed URL"


admin.site.register(Provider)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdvertisementPanel, PanelAdmin)
