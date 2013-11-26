from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.conf import settings


urlpatterns = patterns('',
    url(r'^data/', include('advertisements.urls', namespace='advert')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )