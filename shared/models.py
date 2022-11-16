from django.db import models
from django.utils.safestring import mark_safe
from core.models import BaseModel
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField

class HomePageBanner(BaseModel):
    title = models.CharField(max_length = 200)
    short_description = models.TextField(blank = True,null=True)
    image = models.ImageField(blank=True,upload_to="uploads/shared")
    link = models.CharField(max_length=500,blank=True,null=True)
    def __str__(self):
        return self.title

class HomePageVideo(BaseModel):
    title = models.CharField(max_length=200)
    youtube_url = models.CharField(max_length=500)
    def __str__(self):
        return self.title


class Testimonial(BaseModel):
    image = models.ImageField(blank=True,upload_to="uploads/profile")
    author_name = models.CharField(max_length=50)
    author_title = models.CharField(max_length=50,null=True,blank=True)
    comment = models.TextField()
    def __str__(self):
        return self.author_name

class Message(BaseModel):
    image = models.ImageField(blank=True,upload_to="uploads/profile")
    author_name = models.CharField(max_length=50)
    author_title = models.CharField(max_length=50,null=True,blank=True)
    comment = models.TextField()
    def __str__(self):
        return self.author_name

class Brochure(BaseModel):
    title = models.CharField(max_length=200,blank=True,null=True)
    brochure = models.FileField(upload_to="uploads/pdf",validators=[FileExtensionValidator(allowed_extensions=['pdf'])],blank=True)

class SiteText(models.Model):
    field_name = models.CharField(max_length=50)
    text = HTMLField(null=True,blank=True)
    help_text = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.field_name

class Career(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10,blank=True,null=True)
    message = models.TextField(null=True,blank=True)
    resume = models.FileField(upload_to="uploads/resume")
    def __str__(self):
        return self.name

    @property
    def resume_file(self):
        return mark_safe('<a target="blank" href="'+self.resume.url+'">Resume</a>');

    
    
