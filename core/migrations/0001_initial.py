# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table(u'core_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'core', ['Brand'])

        # Adding model 'ProductType'
        db.create_table(u'core_producttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'core', ['ProductType'])

        # Adding model 'BaseColor'
        db.create_table(u'core_basecolor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['BaseColor'])

        # Adding model 'ColorPattern'
        db.create_table(u'core_colorpattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('family_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=32, null=True, blank=True)),
            ('swatch', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('num_of_colors', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_solid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_complex_pattern', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_blackandwhite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('known_names', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
        ))
        db.send_create_signal(u'core', ['ColorPattern'])

        # Adding M2M table for field basecolors on 'ColorPattern'
        db.create_table(u'core_colorpattern_basecolors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('colorpattern', models.ForeignKey(orm[u'core.colorpattern'], null=False)),
            ('basecolor', models.ForeignKey(orm[u'core.basecolor'], null=False))
        ))
        db.create_unique(u'core_colorpattern_basecolors', ['colorpattern_id', 'basecolor_id'])

        # Adding model 'ClothItem'
        db.create_table(u'core_clothitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('path', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brand'])),
            ('has_multiple_colors', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('agegroup', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('photo_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('regular_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('sale_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('percent_off', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('average_rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=1, blank=True)),
            ('is_designer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ClothItem'])

        # Adding M2M table for field palettes on 'ClothItem'
        db.create_table(u'core_clothitem_palettes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clothitem', models.ForeignKey(orm[u'core.clothitem'], null=False)),
            ('colorpattern', models.ForeignKey(orm[u'core.colorpattern'], null=False))
        ))
        db.create_unique(u'core_clothitem_palettes', ['clothitem_id', 'colorpattern_id'])


    def backwards(self, orm):
        # Deleting model 'Brand'
        db.delete_table(u'core_brand')

        # Deleting model 'ProductType'
        db.delete_table(u'core_producttype')

        # Deleting model 'BaseColor'
        db.delete_table(u'core_basecolor')

        # Deleting model 'ColorPattern'
        db.delete_table(u'core_colorpattern')

        # Removing M2M table for field basecolors on 'ColorPattern'
        db.delete_table('core_colorpattern_basecolors')

        # Deleting model 'ClothItem'
        db.delete_table(u'core_clothitem')

        # Removing M2M table for field palettes on 'ClothItem'
        db.delete_table('core_clothitem_palettes')


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
            'percent_off': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
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