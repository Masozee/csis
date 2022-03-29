from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Project)
admin.site.register(Department)
admin.site.register(Event)
admin.site.register(Publication_category)
admin.site.register(Publication)
admin.site.register(Person)
admin.site.register(News)

