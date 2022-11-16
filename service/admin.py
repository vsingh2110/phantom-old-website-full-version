from django.contrib import admin

from .models import *

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    model = Service
    prepopulated_fields = {'slug': ('name',), }

admin.site.register(Service,ServiceAdmin)


