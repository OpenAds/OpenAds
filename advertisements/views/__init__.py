from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.signing import TimestampSigner, BadSignature
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin, FormMessagesMixin
from advertisements.models import Advertisement, Provider
from advertisements.forms import AdvertisementURLForm, AdvertisementRequestForm
from advertisements.views.mixins import ProviderPermissionRequired, AdvertLoader, PanelLoadMixin


class ClickRegisterView(View):
    def get(self, request, *args, **kwargs):
        signer = TimestampSigner()
        try:
            ad_pk = signer.unsign(kwargs["ad_identifier"])
        except BadSignature:
            raise Http404
        advert = get_object_or_404(Advertisement, pk=ad_pk)

        advert.clicked()

        return HttpResponseRedirect(advert.url)


class TopAdView(TemplateView):
    template_name = "advertisements/top_ad.html"

    def get_context_data(self, **kwargs):
        context = super(TopAdView, self).get_context_data(**kwargs)

        context['advert'] = Advertisement.objects.filter(
            ad_type=Advertisement.TOP_AD,
            status=Advertisement.ACTIVE
        ).get_single_random()

        return context

    def get(self, request, *args, **kwargs):

        if not Advertisement.objects.filter(ad_type=Advertisement.TOP_AD, status=Advertisement.ACTIVE).exists():
            return HttpResponse("No adverts") # TODO: Placeholder
        return super(TopAdView, self).get(request, *args, **kwargs)


class SideAdView(TemplateView):
    template_name = "advertisements/side_ads.html"

    def get_context_data(self, **kwargs):
        context = super(SideAdView, self).get_context_data(**kwargs)

        context['adverts'] = Advertisement.objects.filter(
            ad_type=Advertisement.SIDE_AD,
            status=Advertisement.ACTIVE
        ).get_sample_random()

        return context

    def get(self, request, *args, **kwargs):

        if not Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD, status=Advertisement.ACTIVE).exists():
            return HttpResponse("No adverts")  # TODO: Placeholder
        return super(SideAdView, self).get(request, *args, **kwargs)


class PanelAdView(PanelLoadMixin, TemplateView):
    def get_template_names(self):
        return []


class PreviewView(SuperuserRequiredMixin, TemplateView):
    template_name = 'advertisements/preview.html'

    def get_context_data(self, **kwargs):

        context = super(PreviewView, self).get_context_data(**kwargs)

        context["width"] = kwargs["width"]
        context["height"] = kwargs["height"]
        context["cols"] = range(int(kwargs["cols"]))
        context["rows"] = range(int(kwargs["rows"]))

        return context


class ProviderPermissionRedirectView(ProviderPermissionRequired, View):
    def get(self, request, *args, **kwargs):
        if self.is_superuser:
            # User is an admin, and should see the list view
            return HttpResponseRedirect(reverse('provider:list'))
        else:
            # User is a provider, and should be directed to their provider page
            return HttpResponseRedirect(reverse('provider:stats', args=[self.provider.pk]))


class ProviderListView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'advertisements/statistics/provider_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProviderListView, self).get_context_data(**kwargs)

        # User is a superuser, so this is their home
        context["is_home"] = True

        # A list of all providers, sorted alphabetically
        context["providers"] = Provider.objects.order_by('name')

        return context


class ProviderStatisticsView(ProviderPermissionRequired, TemplateView):
    template_name = "advertisements/statistics/provider_statistics.html"

    def get_context_data(self, **kwargs):
        context = super(ProviderStatisticsView, self).get_context_data(**kwargs)

        context["provider"] = self.provider
        context["active_ads"] = self.provider.advertisement_set.filter(status=Advertisement.ACTIVE)
        context["inactive_ads"] = self.provider.advertisement_set.filter(status=Advertisement.INACTIVE)
        context["pending_ads"] = self.provider.advertisement_set.filter(status=Advertisement.PENDING)

        if not self.is_superuser:
            # User is just a provider
            context["is_home"] = True

        return context


class AdvertStatisticsView(ProviderPermissionRequired, AdvertLoader, FormMessagesMixin, FormView):
    template_name = "advertisements/statistics/advert_statistics.html"
    form_class = AdvertisementURLForm
    form_valid_message = "Your advert URL has been updated!"
    form_invalid_message = "Your advert URL contained errors. Please check the syntax of the URL and try again!"

    def get_initial(self):
        return {
            "url": self.advert.url
        }

    def get_context_data(self, **kwargs):
        context = super(AdvertStatisticsView, self).get_context_data(**kwargs)
        context["history"] = self.advert.click_history(history_days=10)
        return context

    def get_success_url(self):
        return reverse("provider:advert_statistics", args=[self.advert.pk])

    def form_valid(self, form):
        self.advert.url = form.cleaned_data["url"]
        self.advert.save()
        return super(AdvertStatisticsView, self).form_valid(form)


class ProviderRequestView(ProviderPermissionRequired, FormMessagesMixin, FormView):
    template_name = "advertisements/statistics/request_form.html"

    form_class = AdvertisementRequestForm
    form_valid_message = "The advertisement request has been sent!"
    form_invalid_message = "There were errors in your request. Please correct them and resubmit the request."

    advert = None

    def get_form_kwargs(self):
        current_kwargs = super(ProviderRequestView, self).get_form_kwargs()
        current_kwargs["instance"] = Advertisement(
            provider=self.provider,
            status=Advertisement.PENDING,
        )
        return current_kwargs

    def form_valid(self, form):
        self.advert = form.save()
        return super(ProviderRequestView, self).form_valid(form)

    def get_success_url(self):
        return reverse("provider:advert_statistics", args=[self.advert.pk])
