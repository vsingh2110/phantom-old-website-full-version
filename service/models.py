from django.db import models
from core.models import BaseModel
from tinymce.models import HTMLField

class Service(BaseModel):
    slug = models.SlugField(max_length=250, unique=True,db_index=True)
    name = models.CharField(max_length=250)
    priority = models.IntegerField(default = 10)
    description = HTMLField(null=True,blank=True)
    def __str__(self):
        return self.name
