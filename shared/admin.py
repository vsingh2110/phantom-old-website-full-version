from django.contrib import admin
from .models import *

class HomePageBannerAdmin(admin.ModelAdmin):
    model = HomePageBanner

class HomePageVideoAdmin(admin.ModelAdmin):
    model = HomePageVideo

class TestimonialsAdmin(admin.ModelAdmin):
    model = Testimonial

class MessageAdmin(admin.ModelAdmin):
    model = Message

class BrochureAdmin(admin.ModelAdmin):
    model = Brochure

class SiteTextAdmin(admin.ModelAdmin):
    model = SiteText
    list_display = ('field_name','help_text')

class CareerAdmin(admin.ModelAdmin):
    model = Career
    list_display = ('name','email','phone','resume_file')

admin.site.register(HomePageBanner,HomePageBannerAdmin)
admin.site.register(HomePageVideo,HomePageVideoAdmin)
admin.site.register(Testimonial,TestimonialsAdmin)
admin.site.register(Brochure,BrochureAdmin)
admin.site.register(SiteText,SiteTextAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Career,CareerAdmin)

