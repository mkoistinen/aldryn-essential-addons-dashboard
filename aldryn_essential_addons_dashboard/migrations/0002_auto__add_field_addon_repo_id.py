# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Addon.repo_id'
        db.add_column(u'aldryn_essential_addons_dashboard_addon', 'repo_id',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Addon.repo_id'
        db.delete_column(u'aldryn_essential_addons_dashboard_addon', 'repo_id')


    models = {
        u'aldryn_essential_addons_dashboard.addon': {
            'Meta': {'object_name': 'Addon'},
            'build_passing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'component_of'", 'blank': 'True', 'through': u"orm['aldryn_essential_addons_dashboard.Dependency']", 'to': u"orm['aldryn_essential_addons_dashboard.Addon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_django_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'max_python_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'open_source': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'repo_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '1024'}),
            'version': ('versionfield.VersionField', [], {'blank': 'True'})
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