from django.db import models
from django.core.validators import FileExtensionValidator
from core.models import BaseModel
from tinymce.models import HTMLField

# Create your models here.

class Category(BaseModel):
    slug = models.SlugField(max_length=250, unique=True,db_index=True)
    name = models.CharField(max_length=250)
    priority = models.IntegerField(default = 10)
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True,db_index=True)
    main_image = models.ImageField(blank=True,upload_to="uploads/products",help_text="Preferrable size 510x460")
    summary = models.TextField(blank=True)
    description =  HTMLField(blank=True)
    overview = HTMLField(blank=True)
    features = HTMLField(blank=True)
    technical_features = HTMLField(blank=True)
    benefits = HTMLField(blank=True)
    priority = models.IntegerField(default = 10)
    category = models.ForeignKey(Category,related_name="products",null=True, on_delete=models.SET_NULL)
    brochure = models.FileField(upload_to="uploads/pdf",validators=[FileExtensionValidator(allowed_extensions=['pdf'])],blank=True)
    def __str__(self):
        return self.name

class ProductImage(BaseModel):
    alt = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to="uploads/products")
    product = models.ForeignKey(Product,related_name="images", on_delete=models.CASCADE)
    def __str__(self):
        return self.alt

class Feature(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,db_index=True)
    priority = models.IntegerField(default = 10)
    def __str__(self):
        return self.name

class ProductFeatureRelation(models.Model):
    product = models.ForeignKey(Product,related_name="feature_relation", on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature,related_name="product_relation", on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
    unique_together = ((product,feature,),)
    def __str__(self):
        return self.feature.name
