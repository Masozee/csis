from unicodedata import category
from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import *


class projectadmin(admin.ModelAdmin):
    list_display = ('title', 'dept','member', 'periode_start', 'periode_end', 'publish')
    list_filter = ('publish','department')
    search_fields = ['title',]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')

    def member(self, obj):
        return "\n, ".join([p.name for p in obj.project_member.all()])
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])
      

    
admin.site.register(Project, projectadmin)


admin.site.register(Department)

class eventadmin(admin.ModelAdmin):
    list_display = ('title', 'dept','date_start','date_end', 'project', 'publish')
    list_filter = ('publish','department')
    search_fields = ['title',]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ('project',)
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])
admin.site.register(Event, eventadmin)

class pubcatadmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Publication_category, pubcatadmin)

class publicationadmin(admin.ModelAdmin):
    list_display = ('title','author', 'category','dept', 'project', 'publish')
    list_filter = ('publish','department', 'category')
    search_fields = ['title','authors__name']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ('project',)
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

    def author(self, obj):
        return "\n, ".join([p.name for p in obj.authors.all()])

admin.site.register(Publication, publicationadmin)

class personadmin(admin.ModelAdmin):
    list_display = ('name','position','organization','category','dept', 'is_active')
    list_filter = ('category','department',)
    search_fields = ['name','organization']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

admin.site.register(Person, personadmin)

class newsadmin(admin.ModelAdmin):
    list_display = ('title','date_release','publish')
    search_fields = ['title']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    
admin.site.register(News, newsadmin)

