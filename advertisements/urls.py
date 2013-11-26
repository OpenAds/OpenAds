from django.conf.urls import patterns, include, url
from .views import ClickRegisterView, TopAdView, SideAdView

urlpatterns = patterns('advertisements.views',
    url(r'^c/(?P<ad_identifier>\d+:.+)/$', ClickRegisterView.as_view(), name='go'),
    url(r'^top/$', TopAdView.as_view(), name='top'),
    url(r'^sides/$', SideAdView.as_view(), name='side'),

    url(r'^providers/$', 'providers_all'),
    url(r'^provider/(?P<provider_pk>\d+)/request/$', 'provider_request'),
    url(r'^provider/(?P<provider_pk>\d+)/$', 'view_provider_statistics'),
    url(r'^advertisement/(?P<advert_pk>\d+)/$', 'view_advert_statistics', name="advert_statistics"),
    url(r'^$', 'go_to_providers'),
)