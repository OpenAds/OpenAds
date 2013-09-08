from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def superuser_or_provider(function):
    def authenticate_and_continue(*args, **kwargs):
        request = args[0]
        if request.user.is_superuser:
            return function(*args, **kwargs)
        if hasattr(request.user, 'provider'):
            return function(*args, **kwargs)
        return HttpResponseRedirect(reverse('accounts:logout'))
    return authenticate_and_continue
