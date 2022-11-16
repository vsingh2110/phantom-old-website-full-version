from rest_framework import serializers
from core.serializers import BaseModelSerializer

from .models import HomePageBanner,Testimonial,HomePageVideo,Message,Career
class HomePageBannerSerializer(BaseModelSerializer):
    class Meta:
        model = HomePageBanner
        fields = "__all__"

class TestimonialSerializer(BaseModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

class MessageSerializer(BaseModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class HomePageVideoSerializer(BaseModelSerializer):
    class Meta:
        model = HomePageVideo
        fields = "__all__"

class CareerSerializer(BaseModelSerializer):
    class Meta:
        model = Career
        exclude = ('created_date','modified_date','show_on_site',)
