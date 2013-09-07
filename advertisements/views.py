from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from advertisements.models import Advertisement, Provider
from django.contrib.auth.decorators import login_required


def click_register(request, ad_pk):
    advert = get_object_or_404(Advertisement, pk=ad_pk)

    advert.clicked()

    return HttpResponseRedirect(advert.url)


def top_ad(request):
    if not Advertisement.objects.filter(ad_type=Advertisement.TOP_AD, enabled=True).exists():
        return HttpResponse("No adverts") # TODO: Placeholder
    advert = Advertisement.objects.filter(ad_type=Advertisement.TOP_AD, enabled=True).order_by('?')[0]

    return render(request, 'advertisements/top_ad.html', {
        "advert": advert,
    })


def side_ads(request):
    if not Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD, enabled=True).exists():
        return HttpResponse("No adverts")  # TODO: Placeholder
    adverts = Advertisement.objects.filter(ad_type=Advertisement.SIDE_AD, enabled=True).order_by('?')[:4]

    return render(request, 'advertisements/side_ads.html', {
        "adverts": adverts,
    })


@login_required
def view_provider_statistics(request, provider_pk):
    provider = get_object_or_404(Provider, pk=provider_pk)

    return render(request, 'advertisements/statistics/provider_statistics.html', {
        "provider": provider,
    })
