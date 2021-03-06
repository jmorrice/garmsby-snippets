# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Design.full_img'
        db.delete_column(u'designs_design', 'full_img')

        # Adding field 'Design.tee_colour'
        db.add_column(u'designs_design', 'tee_colour',
                      self.gf('django.db.models.fields.CharField')(default='White', max_length=50),
                      keep_default=False)

        # Adding field 'Design.preview_colour'
        db.add_column(u'designs_design', 'preview_colour',
                      self.gf('django.db.models.fields.CharField')(default='White', max_length=50),
                      keep_default=False)

        # Adding field 'Design.design_pic'
        db.add_column(u'designs_design', 'design_pic',
                      self.gf('sorl.thumbnail.fields.ImageField')(default='designs/default_design_pic.png', max_length=100),
                      keep_default=False)

        # Adding field 'Design.tee_pic'
        db.add_column(u'designs_design', 'tee_pic',
                      self.gf('sorl.thumbnail.fields.ImageField')(default='designs/default_tee_pic.png', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Design.full_img'
        db.add_column(u'designs_design', 'full_img',
                      self.gf('django.db.models.fields.files.ImageField')(default='designs/default_design.png', max_length=100),
                      keep_default=False)

        # Deleting field 'Design.tee_colour'
        db.delete_column(u'designs_design', 'tee_colour')

        # Deleting field 'Design.preview_colour'
        db.delete_column(u'designs_design', 'preview_colour')

        # Deleting field 'Design.design_pic'
        db.delete_column(u'designs_design', 'design_pic')

        # Deleting field 'Design.tee_pic'
        db.delete_column(u'designs_design', 'tee_pic')


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
            'design_pic': ('sorl.thumbnail.fields.ImageField', [], {'default': "'designs/default_design_pic.png'", 'max_length': '100'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'DefaultDesign'", 'max_length': '50'}),
            'preview_colour': ('django.db.models.fields.CharField', [], {'default': "'White'", 'max_length': '50'}),
            'story': ('django.db.models.fields.TextField', [], {'default': "'Default Story'", 'max_length': '250'}),
            'tee_colour': ('django.db.models.fields.CharField', [], {'default': "'White'", 'max_length': '50'}),
            'tee_pic': ('sorl.thumbnail.fields.ImageField', [], {'default': "'designs/default_tee_pic.png'", 'max_length': '100'})
        },
        u'designs.like': {
            'Meta': {'object_name': 'Like'},
            'design': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['designs.Design']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['designs']