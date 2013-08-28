# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Advertisement.enabled'
        db.add_column(u'advertisements_advertisement', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Advertisement.enabled'
        db.delete_column(u'advertisements_advertisement', 'enabled')


    models = {
        u'advertisements.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'ad_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {'max_length': '64'}),
            'image_width': ('django.db.models.fields.IntegerField', [], {'max_length': '64'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertisements.Provider']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'advertisements.click': {
            'Meta': {'object_name': 'Click'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertisements.Advertisement']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'advertisements.provider': {
            'Meta': {'object_name': 'Provider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['advertisements']