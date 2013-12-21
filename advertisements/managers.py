from random import randint, sample
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet


class AdvertisementQueryset(QuerySet):
    def get_single_random(self):
        count = self.aggregate(count=Count('id'))['count']

        if not count:
            return None

        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def get_sample_random(self, no_items=4):
        count = self.aggregate(count=Count('id'))['count']

        if not count:
            # There are no adverts
            return None

        if count <= no_items:
            # There are not enough adverts for the number of items. Just return what we have got
            return self.all()

        random_positions = sample(range(count), no_items)
        adverts = []

        for position in random_positions:
            adverts.append(self.all()[position])

        return adverts


class AdvertisementManager(models.Manager):
    def get_queryset(self):
        return AdvertisementQueryset(model=self.model, using=self._db)
