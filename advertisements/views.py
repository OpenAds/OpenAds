from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from advertisements.models import Advertisement


def click_register(request, ad_pk):
    advert = get_object_or_404(Advertisement, pk=ad_pk)

    advert.clicked()

    return HttpResponseRedirect(advert.url)
