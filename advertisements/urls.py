from django.conf.urls import patterns, include, url
from .views import ClickRegisterView, TopAdView, SideAdView, ProviderStatisticsView


providerpatterns = patterns('advertisements.views',

    url(r'$', ProviderStatisticsView.as_view(), name="stats"),

    url(r'^request/$', 'provider_request', name="request"),
    url(r'^ad/(?P<advert_pk>\d+)/$', 'view_advert_statistics', name="advert_statistics"),
)

urlpatterns = patterns('advertisements.views',
    url(r'^c/(?P<ad_identifier>\d+:.+)/$', ClickRegisterView.as_view(), name='go'),
    url(r'^top/$', TopAdView.as_view(), name='top'),
    url(r'^sides/$', SideAdView.as_view(), name='side'),

    url(r'^$', 'go_to_providers', name="providers"),
    url(r'^provider/', include(providerpatterns, namespace='provider')),
)