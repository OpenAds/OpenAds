from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin
from advertisements.models import Advertisement, AdvertisementPanel, Provider


class ProviderAccessPermissionMixin(object):
    def __init__(self, *args, **kwargs):
        super(ProviderAccessPermissionMixin, self).__init__(*args, **kwargs)

        self.is_superuser = False
        self.provider = None

    def dispatch(self, request, *args, **kwargs):
        self.is_superuser = request.user.is_superuser

        if self.is_superuser:
            # The user is a superuser, and the provider_pk should be in the url
            if "provider_pk" in kwargs:
                self.provider = get_object_or_404(Provider, pk=kwargs["provider_pk"])
        elif hasattr(request.user, 'provider'):
            # The user is a provider (and has one assigned to their account)
            self.provider = request.user.provider
        else:
            # The user is just a normal user, and should not get access
            raise PermissionDenied

        return super(ProviderAccessPermissionMixin, self).dispatch(request, *args, **kwargs)


class ProviderPermissionRequired(LoginRequiredMixin, ProviderAccessPermissionMixin):
    pass


class AdvertLoader(object):
    def __init__(self, *args, **kwargs):
        super(AdvertLoader, self).__init__(*args, **kwargs)
        self.advert = None

    def dispatch(self, request, *args, **kwargs):
        if self.is_superuser:
            self.advert = get_object_or_404(Advertisement, pk=kwargs["advert_pk"])
        else:
            self.advert = get_object_or_404(self.provider.advertisement_set, pk=kwargs["advert_pk"])
        return super(AdvertLoader, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AdvertLoader, self).get_context_data(**kwargs)
        context["advert"] = self.advert

        return context


class PanelLoadMixin(object):
    panel = None

    def dispatch(self, request, *args, **kwargs):

        self.panel = get_object_or_404(AdvertisementPanel, pk=kwargs['panel_pk'])

        return super(PanelLoadMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(PanelLoadMixin, self).get_context_data(**kwargs)

        context["panel"] = self.panel

        return context