from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Slider

class SliderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['title', 'url', 'image', 'show', 'date_created']
admin.site.register(Slider, SliderAdmin)
