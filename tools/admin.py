from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from .models import  *
# Register your models here.


class shortadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ShortenWord','Url', 'kategori', 'publish')
    search_fields = ['ShortenWord',]
admin.site.register( Shorten, shortadmin)
