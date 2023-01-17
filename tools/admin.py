from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html


from .models import  *
# Register your models here.


class shortadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Judul','shorten','Url', 'kategori', 'times_followed', 'publish')
    search_fields = ['ShortenWord',]
    list_filter = ('kategori',)

    def shorten(self, obj):
        return format_html('<a href="https://csis.or.id/{}/{}">https://csis.or.id/{}/{}</a>', obj.kategori, obj.ShortenWord, obj.kategori, obj.ShortenWord,)

admin.site.register( Shorten, shortadmin)
