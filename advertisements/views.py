from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from advertisements.models import Advertisement


def click_register(request, ad_pk):
    advert = get_object_or_404(Advertisement, pk=ad_pk)

    advert.clicked()

    return HttpResponseRedirect(advert.url)


def top_ad(request):
    if not Advertisement.objects.exists():
        return HttpResponse("No adverts") # TODO: Placeholder
    adverts = Advertisement.objects.order_by('?')[:4]

    return render(request, 'advertisements/top_ad.html', {
        "adverts": adverts,
    })