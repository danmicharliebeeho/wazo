# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ClothItem.percent_off'
        db.alter_column(u'core_clothitem', 'percent_off', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'ClothItem.sale_price'
        db.alter_column(u'core_clothitem', 'sale_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'ClothItem.percent_off'
        db.alter_column(u'core_clothitem', 'percent_off', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'ClothItem.sale_price'
        db.alter_column(u'core_clothitem', 'sale_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2))

    models = {
        u'core.basecolor': {
            'Meta': {'object_name': 'BaseColor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'core.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'core.clothitem': {
            'Meta': {'object_name': 'ClothItem'},
            'agegroup': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'average_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brand']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'has_multiple_colors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_designer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'palettes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.ColorPattern']", 'symmetrical': 'False'}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'percent_off': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'photo_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.colorpattern': {
            'Meta': {'object_name': 'ColorPattern'},
            'basecolors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.BaseColor']", 'symmetrical': 'False'}),
            'family_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blackandwhite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_complex_pattern': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_solid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'known_names': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'num_of_colors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'swatch': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.producttype': {
            'Meta': {'object_name': 'ProductType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['core']