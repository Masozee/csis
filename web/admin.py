from unicodedata import category
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *


@admin.action(description='Mark selected stories as published')
def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)

@admin.action(description='Unpublish')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(publish=False)


class deptAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Department, deptAdmin)

class topicAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'parent', 'date_created', 'date_modified', 'publish')
    search_fields = ['name',]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['parent']
    list_per_page=15

admin.site.register(Topic, topicAdmin)

class projectadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'dept','member', 'periode_start', 'periode_end', 'publish')
    list_filter = ('publish','department')
    search_fields = ['title','department','project_member' ]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['department', 'project_member', 'donor', 'project_topic']

    def member(self, obj):
        return "\n, ".join([p.name for p in obj.project_member.all()])
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])
      
    
admin.site.register(Project, projectadmin)


class sessionAdmin(admin.TabularInline):
    model = EventSession
    autocomplete_fields = ['Speakers']

class eventadmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [
        sessionAdmin,
    ]

    list_display = ('title', 'dept','date_start','date_end','speakers', 'project', 'publish')
    list_filter = ('publish','department')
    search_fields = ['title',]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['project', 'speaker', 'department', 'topic', 'opening_speech', 'Moderator', 'closing_remarks']
    actions = [make_published]
    list_per_page=15
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

    def speakers(self, obj):
        return "\n, ".join([p.name for p in obj.speaker.all()])

admin.site.register(Event, eventadmin)

class pubcatadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id','name', 'keterangan', 'background')
    search_fields = ['name',]
admin.site.register(Publication_category, pubcatadmin)

class DonorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Nama', 'url', 'publish')
    search_fields = ['Nama']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
admin.site.register(Donor, DonorAdmin)

class publicationadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title','author', 'category','date_publish','dept', 'project', 'publish', 'donors')
    list_filter = ('publish','department', 'category')
    search_fields = ['title','authors__name','donor__Nama']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['project', 'editor', 'authors','department', 'category', 'topic', 'donor']
    actions = [make_published]
    list_per_page=15
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

    def author(self, obj):
        return "\n, ".join([p.name for p in obj.authors.all()])

    def donors(self, obj):
        return "\n, ".join([p.Nama for p in obj.donor.all()])
    def save_model(self, request, obj, form, change):
        if obj.id == None:
           obj.added_by = request.user
           super().save_model(request, obj, form, change)

        else:

           super().save_model(request, obj, form, change)

admin.site.register(Publication, publicationadmin)

class personadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name','position','organization','category','dept', 'is_active')
    list_filter = ('category','department',)
    search_fields = ['name','organization']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified', )
    autocomplete_fields = ['department', 'expertise']
    actions = [make_published]
    list_per_page=15
        
    def dept(self, obj):
        return "\n, ".join([p.name for p in obj.department.all()])

admin.site.register(Person, personadmin)

class news_admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title','date_release','publish')
    search_fields = ['title']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    actions = [make_published]
    
admin.site.register(News, news_admin)


class foundation_admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Title','members','date_created','publish')
    search_fields = ['title']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['member', ]
    actions = [make_published]

    def members(self, obj):
        return "\n, ".join([p.name for p in obj.member.all()])
    
admin.site.register(Foundation, foundation_admin)


class external_admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'author','source','category', 'date', 'publish')
    list_display_links = ('title', 'author')
    list_filter = ('category', 'publish',)
    search_fields = [('title', 'source')]
    date_hierarchy = 'date'
    readonly_fields = ('date_created', 'date_modified')
    autocomplete_fields = ['author', ]
    actions = [make_published]
admin.site.register(ExternalPublications, external_admin)


