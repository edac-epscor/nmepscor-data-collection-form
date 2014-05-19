# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'metadataModel'
        db.create_table(u'builder_metadatamodel', (
            ('submissionID', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('started', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('finalized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('finalizedTime', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('mdForm', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'builder', ['metadataModel'])


    def backwards(self, orm):
        # Deleting model 'metadataModel'
        db.delete_table(u'builder_metadatamodel')


    models = {
        u'builder.metadatamodel': {
            'Meta': {'object_name': 'metadataModel'},
            'finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'finalizedTime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mdForm': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'submissionID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['builder']