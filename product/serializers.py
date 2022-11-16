from rest_framework import serializers

from core.serializers import BaseModelSerializer
from .models import Product,ProductImage,ProductFeatureRelation,Feature

class FeatureSerializer(BaseModelSerializer):
    class Meta:
        model = Feature
        fields = ('name','slug',)

class FeatureRelationSerializer(BaseModelSerializer):
    feature = FeatureSerializer()
    class Meta:
        model = ProductFeatureRelation
        fields = ('feature','value',)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image','alt')

class ProductDetailSerializer(BaseModelSerializer):
    images = ProductImageSerializer(many=True)
    tech_features = FeatureRelationSerializer(many=True,source="feature_relation")
    class Meta:
        model = Product
        fields = "__all__"

class ProductListSerializer(BaseModelSerializer):
    category = serializers.ReadOnlyField(source="category.name")
    value = serializers.ReadOnlyField(source="name")
    class Meta:
        model = Product
        fields = ('name','slug','main_image','value','category')

