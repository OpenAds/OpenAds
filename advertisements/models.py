from django.db import models
import uuid
import os


class Provider(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


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

    ad_type = models.CharField(max_length=1, choices=AD_TYPES)
    provider = models.ForeignKey(Provider)
    url = models.URLField(max_length=255)
    enabled = models.BooleanField(default=True)

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


class Click(models.Model):
    ad = models.ForeignKey(Advertisement)
    date = models.DateTimeField(auto_now_add=True)

