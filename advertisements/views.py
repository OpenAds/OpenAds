from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from advertisements.models import Advertisement, Provider
from advertisements.decorators import superuser_or_provider
from advertisements.forms import AdvertisementURLForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages


def click_register(request, ad_pk):
    advert = get_object_or_404(Advertisement, pk=ad_pk)

    advert.clicked()

    return HttpResponseRedirect(advert.url)


def top_ad(request):
    if not Advertisement.objects.filter(ad_type=Advertisement.TOP_AD, status=Advertisement.ACTIVE).exists():
        return HttpResponse("No adverts") # TODO: Placeholder
    advert = Advertisement.objects.filter(ad_type=Advertisement.TOP_AD, status=Advertisement.ACTIVE).order_by('?')[0]

    return render(request, 'advertisements/top_ad.html', {
        "advert": advert,
    })


def side_ads(request):
    if not Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD, status=Advertisement.ACTIVE).exists():
        return HttpResponse("No adverts")  # TODO: Placeholder
    adverts = Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD, status=Advertisement.ACTIVE).order_by('?')[:4]

    return render(request, 'advertisements/side_ads.html', {
        "adverts": adverts,
    })


@superuser_or_provider
@login_required
def go_to_providers(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('advertisements.views.providers_all'))
    else:
        return HttpResponseRedirect(
            reverse('advertisements.views.view_provider_statistics', args=[request.user.provider.pk])
        )


@superuser_or_provider
@login_required
def providers_all(request):
    if not request.user.is_superuser:
        raise Http404
    providers = Provider.objects.all()

    return render(request, 'advertisements/statistics/provider_list.html', {
        "providers": providers,
    })

@superuser_or_provider
@login_required
def view_provider_statistics(request, provider_pk):
    if not request.user.is_superuser:
        if request.user.provider.pk != long(provider_pk):
            raise Http404
    provider = get_object_or_404(Provider, pk=provider_pk)

    return render(request, 'advertisements/statistics/provider_statistics.html', {
        "provider": provider,
        "active_ads": provider.advertisement_set.filter(status=Advertisement.ACTIVE),
        "inactive_ads": provider.advertisement_set.filter(status=Advertisement.INACTIVE),
        "pending_ads": provider.advertisement_set.filter(status=Advertisement.PENDING),
    })


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
