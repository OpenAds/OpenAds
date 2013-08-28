# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provider'
        db.create_table(u'advertisements_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'advertisements', ['Provider'])

        # Adding model 'Advertisement'
        db.create_table(u'advertisements_advertisement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertisements.Provider'])),
            ('image_height', self.gf('django.db.models.fields.IntegerField')(max_length=64)),
            ('image_width', self.gf('django.db.models.fields.IntegerField')(max_length=64)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'advertisements', ['Advertisement'])

        # Adding model 'Click'
        db.create_table(u'advertisements_click', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertisements.Advertisement'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'advertisements', ['Click'])


    def backwards(self, orm):
        # Deleting model 'Provider'
        db.delete_table(u'advertisements_provider')

        # Deleting model 'Advertisement'
        db.delete_table(u'advertisements_advertisement')

        # Deleting model 'Click'
        db.delete_table(u'advertisements_click')


    models = {
        u'advertisements.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'ad_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {'max_length': '64'}),
            'image_width': ('django.db.models.fields.IntegerField', [], {'max_length': '64'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertisements.Provider']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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