# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dependency'
        db.create_table(u'aldryn_essential_addons_dashboard_dependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('addon', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name=u'addon', to=orm['aldryn_essential_addons_dashboard.Addon'])),
            ('dependency', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name=u'dependency', to=orm['aldryn_essential_addons_dashboard.Addon'])),
            ('optional', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aldryn_essential_addons_dashboard', ['Dependency'])

        # Adding model 'Addon'
        db.create_table(u'aldryn_essential_addons_dashboard_addon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('repo_slug', self.gf('django.db.models.fields.CharField')(default=u'', unique=True, max_length=255)),
            ('auth_digest', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('open_source', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('version', self.gf('versionfield.VersionField')(blank=True)),
            ('max_python_version', self.gf('versionfield.VersionField')(null=True, blank=True)),
            ('max_django_version', self.gf('versionfield.VersionField')(null=True, blank=True)),
            ('build_passing', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'aldryn_essential_addons_dashboard', ['Addon'])


    def backwards(self, orm):
        # Deleting model 'Dependency'
        db.delete_table(u'aldryn_essential_addons_dashboard_dependency')

        # Deleting model 'Addon'
        db.delete_table(u'aldryn_essential_addons_dashboard_addon')


    models = {
        u'aldryn_essential_addons_dashboard.addon': {
            'Meta': {'object_name': 'Addon'},
            'auth_digest': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'build_passing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'component_of'", 'blank': 'True', 'through': u"orm['aldryn_essential_addons_dashboard.Dependency']", 'to': u"orm['aldryn_essential_addons_dashboard.Addon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_django_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'max_python_version': ('versionfield.VersionField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'open_source': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'repo_slug': ('django.db.models.fields.CharField', [], {'default': "u''", 'unique': 'True', 'max_length': '255'}),
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