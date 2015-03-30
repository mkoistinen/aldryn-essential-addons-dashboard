# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Addon.last_successful_build'
        db.add_column(u'aldryn_essential_addons_dashboard_addon', 'last_successful_build',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Addon.last_successful_build'
        db.delete_column(u'aldryn_essential_addons_dashboard_addon', 'last_successful_build')


    models = {
        u'aldryn_essential_addons_dashboard.addon': {
            'Meta': {'object_name': 'Addon'},
            'auth_digest': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'build_passing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'component_of'", 'blank': 'True', 'through': u"orm['aldryn_essential_addons_dashboard.Dependency']", 'to': u"orm['aldryn_essential_addons_dashboard.Addon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_successful_build': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_webhook_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'max_django_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'max_python_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'min_django_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'min_python_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'open_source': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'repo_slug': ('django.db.models.fields.CharField', [], {'default': "u''", 'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '255'}),
            'version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'})
        },
        u'aldryn_essential_addons_dashboard.dependency': {
            'Meta': {'object_name': 'Dependency'},
            'addon': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'addon'", 'to': u"orm['aldryn_essential_addons_dashboard.Addon']"}),
            'dependency': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'dependency'", 'to': u"orm['aldryn_essential_addons_dashboard.Addon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optional': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['aldryn_essential_addons_dashboard']