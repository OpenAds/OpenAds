from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=255)


class Advertisement(models.Model):
    TOP_AD = 't'
    SIDE_AD = 's'

    AD_TYPES = (
        (TOP_AD, 'Banner Ad'),
        (SIDE_AD, 'Side Ad'),
    )

    ad_type = models.CharField(max_length=1, choices=AD_TYPES)
    provider = models.ForeignKey(Provider)

    image_height = models.IntegerField(max_length=64)
    image_width = models.IntegerField(max_length=64)

    image = models.ImageField(max_length=255, upload_to='adverts')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{} ()".format(self.provider.name, self.get_ad_type_display())


class Click(models.Model):
    ad = models.ForeignKey(Advertisement)
    date = models.DateTimeField(auto_now_add=True)

