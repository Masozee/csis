from unicodedata import category
from django.contrib import admin
from django.utils.html import format_html
from jmespath import search

# Register your models here.
from .models import *

class deptAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Department, deptAdmin)


class projectadmin(admin.ModelAdmin):
    list_display = ('title', 'dept','member', 'periode_start', 'periode_end', 'publish')
    list_filter = ('publish','department')
    search_fields = ['title','department','project_member' ]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['department', 'project_member']

    def member(self, obj):
        return "\n, ".join([p.name for p in obj.project_member.all()])
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])
      
    
admin.site.register(Project, projectadmin)



class eventadmin(admin.ModelAdmin):
    list_display = ('title', 'dept','date_start','date_end','speakers', 'project', 'publish')
    list_filter = ('publish','department')
    search_fields = ['title',]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['project', 'speaker', 'department']
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

    def speakers(self, obj):
        return "\n, ".join([p.name for p in obj.speaker.all()])

admin.site.register(Event, eventadmin)

class pubcatadmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['name',]
admin.site.register(Publication_category, pubcatadmin)

class publicationadmin(admin.ModelAdmin):
    list_display = ('title','author', 'category','dept', 'project', 'publish')
    list_filter = ('publish','department', 'category')
    search_fields = ['title','authors__name']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['project', 'authors', 'category']
        
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
    autocomplete_fields = ['department']
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

admin.site.register(Person, personadmin)

class newsadmin(admin.ModelAdmin):
    list_display = ('title','date_release','publish')
    search_fields = ['title']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    
admin.site.register(News, newsadmin)

