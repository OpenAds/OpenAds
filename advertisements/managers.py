from random import randint
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet


class AdvertisementQueryset(QuerySet):
    def get_single_random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class AdvertisementManager(models.Manager):
    def get_queryset(self):
        return AdvertisementQueryset(model=self.model, using=self._db)
