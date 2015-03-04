from django.contrib import admin
from .models import BaseColor, ClothItem, ColorPattern


class BaseColorInline(admin.StackedInline):
    model = BaseColor

class ColorPatternAdmin(admin.ModelAdmin):
    inlines = [ BaseColorInline,]

class ClothItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(ColorPattern, ColorPatternAdmin)
admin.site.register(ClothItem, ClothItemAdmin)