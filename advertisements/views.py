from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from advertisements.models import Advertisement, Provider
from advertisements.decorators import superuser_or_provider
from advertisements.forms import AdvertisementURLForm, AdvertisementRequestForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.signing import TimestampSigner, BadSignature
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin, FormValidMessageMixin


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


class ProviderAccessPermissionMixin(LoginRequiredMixin):
    def __init__(self, *args, **kwargs):
        super(ProviderAccessPermissionMixin, self).__init__(*args, **kwargs)

        self.is_superuser = False
        self.provider = None

    def dispatch(self, request, *args, **kwargs):
        self.is_superuser = request.user.is_superuser

        # This is a provider accessing their own page
        if hasattr(request.user, 'provider'):
            # The user is a provider (and has one assigned to their account)
            self.provider = request.user.provider
        else:
            # The user is just a normal user, and should not get access
            raise PermissionDenied

        return super(ProviderAccessPermissionMixin, self).dispatch(request, *args, **kwargs)


class ProviderStatisticsView(ProviderAccessPermissionMixin, TemplateView):
    template_name = "advertisements/statistics/provider_statistics.html"

    def get_context_data(self, **kwargs):
        context = super(ProviderStatisticsView, self).get_context_data(**kwargs)

        context["provider"] = self.provider
        context["active_ads"] = self.provider.advertisement_set.filter(status=Advertisement.ACTIVE)
        context["inactive_ads"] = self.provider.advertisement_set.filter(status=Advertisement.INACTIVE)
        context["pending_ads"] = self.provider.advertisement_set.filter(status=Advertisement.PENDING)

        return context


class AdvertStatisticsView(ProviderAccessPermissionMixin, FormValidMessageMixin, FormView):
    template_name = "advertisements/statistics/advert_statistics.html"
    form_class = AdvertisementURLForm
    form_valid_message = "Your advert URL has been updated!"

    advert = None

    def dispatch(self, request, *args, **kwargs):
        self.advert = get_object_or_404(Advertisement, pk=kwargs["advert_pk"])
        return super(AdvertStatisticsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AdvertStatisticsView, self).get_context_data(**kwargs)
        context["advert"] = self.advert

        return context

    def get_initial(self):
        return {
            "url": self.advert.url
        }

    def get_success_url(self):
        return reverse("advert:provider:advert_statistics", args=[self.advert.pk])

    def form_valid(self, form):
        self.advert.url = form.cleaned_data["url"]
        self.advert.save()
        return super(AdvertStatisticsView, self).form_valid(form)


@superuser_or_provider
@login_required
def view_advert_statistics(request, advert_pk):
    if not request.user.is_superuser:
        if not request.user.provider.advertisement_set.filter(pk=advert_pk).exists():
            raise Http404
    advert = get_object_or_404(Advertisement, pk=advert_pk)

    if request.method == "POST":
        form = AdvertisementURLForm(request.POST)
        if form.is_valid():
            advert.url = form.cleaned_data["url"]
            advert.save()
            messages.success(request, "The URL for your advertisement has been updated!")
        else:
            messages.warning(request, "The URL for your advertisement was not valid!")

    else:
        form = AdvertisementURLForm({"url":advert.url})

    return render(request, 'advertisements/statistics/advert_statistics.html', {
        "advert": advert,
        "history": advert.click_history(history_days=10),
        "form": form
    })


@superuser_or_provider
@login_required
def provider_request(request, provider_pk):
    if not request.user.is_superuser:
        if request.user.provider.pk != long(provider_pk):
            raise Http404

    provider = get_object_or_404(Provider, pk=provider_pk)

    if request.method == "POST":
        advert = Advertisement(
            provider=provider,
            status=Advertisement.PENDING,
        )
        form = AdvertisementRequestForm(request.POST, request.FILES, instance=advert)
        if form.is_valid():
            advert = form.save()
            messages.success(request, "Request has been sent!")
            return HttpResponseRedirect(reverse('advertisements.views.view_advert_statistics', args=[advert.pk]))
        else:
            messages.warning(request, "The request was not valid!")
    else:
        form = AdvertisementRequestForm()

    return render(request, 'advertisements/statistics/request_form.html', {
        "form": form
    })
