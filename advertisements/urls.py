from django.conf.urls import patterns, include, url
from .views import (
    ClickRegisterView,
    TopAdView,
    SideAdView,
    PanelAdView,
    ProviderPermissionRedirectView,
    ProviderListView,
    ProviderStatisticsView,
    AdvertStatisticsView,
    ProviderRequestView
)


providerpatterns = patterns('advertisements.views',

    url(r'^$', ProviderPermissionRedirectView.as_view(), name="home"),
    url(r'^list/$', ProviderListView.as_view(), name='list'),

    url(r'^(?P<provider_pk>\d+)/$', ProviderStatisticsView.as_view(), name="stats"),

    url(r'^(?P<provider_pk>\d+)/request/$', ProviderRequestView.as_view(), name="request"),
    url(r'^ad/(?P<advert_pk>\d+)/$', AdvertStatisticsView.as_view(), name="advert_statistics"),
)

urlpatterns = patterns('advertisements.views',
    url(r'^c/(?P<ad_identifier>\d+:.+)/$', ClickRegisterView.as_view(), name='go'),
    url(r'^(?P<panel_pk>\d+)/$', PanelAdView.as_view()),
    url(r'^top/$', TopAdView.as_view(), name='top'),
    url(r'^sides/$', SideAdView.as_view(), name='side'),
)
