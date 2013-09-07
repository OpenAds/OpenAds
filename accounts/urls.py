from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {
        "template_name": 'accounts/login_form.html',

    }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout')
)
