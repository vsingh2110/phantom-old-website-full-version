from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from core.models import BaseModel

# Create your models here.

class Post(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique=True,db_index=True)
    content = HTMLField()
    summary = models.TextField(null=True,blank=True)
    top_image = models.ImageField(blank=True,upload_to="uploads/posts")
    publish_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
