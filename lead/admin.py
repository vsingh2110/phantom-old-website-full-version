from django.contrib import admin
from .models import *
class LeadAdmin(admin.ModelAdmin):
    model = Lead
    list_display = ('name','email','phone','lead_type','message')
    list_filter = ('lead_type',)

class StateInline(admin.StackedInline):
    model = State
    prepopulated_fields = {'slug': ('name',), }

class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = (StateInline,)
    prepopulated_fields = {'slug': ('name',), }

class CityInline(admin.StackedInline):
    model = City
    prepopulated_fields = {'slug': ('name',), }

class StateAdmin(admin.ModelAdmin):
    model = State
    inlines = (CityInline,)
    prepopulated_fields = {'slug': ('name',), }

class CityAdmin(admin.ModelAdmin):
    model = City
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(Lead,LeadAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(State,StateAdmin)
admin.site.register(City,CityAdmin)
