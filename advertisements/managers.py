from django.db import models
from django.db.models.query import QuerySet


class AdvertisementQueryset(QuerySet):
    pass


class AdvertisementManager(models.Manager):
    def get_queryset(self):
        return AdvertisementQueryset(model=self.model, using=self._db)
