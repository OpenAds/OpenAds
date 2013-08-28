from django.conf.urls import patterns, include, url

urlpatterns = patterns('advertisements.views',
    url(r'^click_register/(?P<ad_pk>\d+)/$', 'click_register'),
    url(r'^top/$', 'top_ad')
)