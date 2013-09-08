from django.db import models
import uuid
import os
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Provider(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def active_ads(self):
        return self.advertisement_set.filter(enabled=True).count()

    def inactive_ads(self):
        return self.advertisement_set.filter(enabled=False).count()

    def total_clicks(self):
        click_count = 0
        for advert in self.advertisement_set.filter(enabled=True):
            click_count += advert.click_set.count()
        return click_count

    def get_absolute_url(self):
        return reverse('advertisements.views.view_provider_statistics', args=[self.pk])


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('resources', filename)


class Advertisement(models.Model):
    TOP_AD = 't'
    SIDE_AD = 's'

    AD_TYPES = (
        (TOP_AD, 'Banner Ad'),
        (SIDE_AD, 'Side Ad'),
    )

    ACTIVE = 'a'
    INACTIVE = 'i'
    PENDING = 'p'

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (PENDING, 'Pending'),
    )

    ad_type = models.CharField(max_length=1, choices=AD_TYPES)
    provider = models.ForeignKey(Provider)
    url = models.URLField(max_length=255)
    enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ACTIVE)

    image_height = models.IntegerField(max_length=64, editable=False)
    image_width = models.IntegerField(max_length=64, editable=False)

    image = models.ImageField(
        max_length=255,
        upload_to=get_file_path,
        height_field='image_height',
        width_field='image_width'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} ({1})".format(self.provider.name, self.get_ad_type_display())

    def clicked(self):
        click = Click(
            ad=self,
        )
        click.save()

        return click

    def is_side(self):
        if self.ad_type == self.SIDE_AD:
            return True
        return False

    def click_history(self, history_days=10):
        today = timezone.now().date()
        click_data = []
        for days_back in reversed(xrange(history_days)):
            date = today - timedelta(days=days_back)
            clicks = self.click_set.filter(
                date__year=date.year,
                date__month=date.month,
                date__day=date.day,
            ).count()
            click_data.append({
                "date": date,
                "clicks": clicks
            })
        return click_data

    def get_absolute_url(self):
        return reverse('advertisements.views.view_advert_statistics', args=[self.pk])


class Click(models.Model):
    ad = models.ForeignKey(Advertisement)
    date = models.DateTimeField(auto_now_add=True)

