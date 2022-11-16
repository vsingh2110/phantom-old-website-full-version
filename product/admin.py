from django.contrib import admin
from .models import *

# Register your models here.

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductFeatureInline(admin.StackedInline):
    model = ProductFeatureRelation

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name',)
    list_filter = ('category',)
    inlines = (ProductImageAdmin,ProductFeatureInline)
    prepopulated_fields = {'slug': ('name',), }

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {'slug': ('name',), }

class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    prepopulated_fields = {'slug': ('name',), }

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Feature,FeatureAdmin)


