from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *

class SliderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'url', 'image', 'show', 'date_created')
admin.site.register(Slider, SliderAdmin)

class CDAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('cdid', 'ket')
admin.site.register(CodebookOrder, CDAdmin)

class CareerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'date_created', 'date_modified')
admin.site.register( Career, CareerAdmin)