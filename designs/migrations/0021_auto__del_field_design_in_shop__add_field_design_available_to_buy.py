# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Design.in_shop'
        db.delete_column(u'designs_design', 'in_shop')

        # Adding field 'Design.available_to_buy'
        db.add_column(u'designs_design', 'available_to_buy',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Design.in_shop'
        db.add_column(u'designs_design', 'in_shop',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Design.available_to_buy'
        db.delete_column(u'designs_design', 'available_to_buy')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'designs.design': {
            'Meta': {'object_name': 'Design'},
            'available_to_buy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'design_pic': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"}),
            'garment': ('django.db.models.fields.CharField', [], {'default': "'garment_tshirt'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_production': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_voting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'past_voting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preview_colour': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '50'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'story': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'tee_colour': ('django.db.models.fields.CharField', [], {'default': "'colour_white'", 'max_length': '50'}),
            'tee_pic': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_agreement_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_agreement_version': ('django.db.models.fields.CharField', [], {'default': "'v1.1'", 'max_length': '10'})
        },
        u'designs.like': {
            'Meta': {'object_name': 'Like'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'design': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['designs.Design']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"})
        },
        u'designs.readynotification': {
            'Meta': {'object_name': 'ReadyNotification'},
            'design': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['designs.Design']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['designs']