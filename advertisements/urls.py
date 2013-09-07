from django.conf.urls import patterns, include, url

urlpatterns = patterns('advertisements.views',
    url(r'^click_register/(?P<ad_pk>\d+)/$', 'click_register'),
    url(r'^top/$', 'top_ad'),
    url(r'^sides/$', 'side_ads'),

    url(r'^provider/(?P<provider_pk>\d+)/$', 'view_provider_statistics'),
    url(r'^advertisement/(?P<advert_pk>\d+)/$', 'view_advert_statistics', name="advert_statistics")
)