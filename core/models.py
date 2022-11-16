from django.db import models

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    show_on_site = models.BooleanField(default=True)
    class Meta:
        abstract = True

