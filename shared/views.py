from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from core.views import BaseAPIView
from relatedviews import mixins
from relatedviews.pagination import NoPagination
from .models import *
from .serializers import *
from relatedviews.filters import MutableDjangoFilterBackend,OrderBackend,CountBackend

class TestimonialView(mixins.ListAPIView):
    queryset = Testimonial.objects.filter(show_on_site=True).all()
    serializer_class = TestimonialSerializer
    pagination_class = NoPagination
    filter_backends = (CountBackend,)

class MessageView(mixins.ListAPIView):
    queryset = Message.objects.filter(show_on_site=True).all()
    serializer_class = MessageSerializer
    pagination_class = NoPagination
    filter_backends = (CountBackend,)

class HomePageBannerView(mixins.ListAPIView):
    queryset = HomePageBanner.objects.filter(show_on_site=True).all()
    serializer_class = HomePageBannerSerializer
    pagination_class = NoPagination
    filter_backends = (CountBackend,)

class HomePageVideoView(mixins.ListAPIView):
    queryset = HomePageVideo.objects.filter(show_on_site=True).all()
    serializer_class = HomePageVideoSerializer
    pagination_class = NoPagination
    filter_backends = (CountBackend,)

def get_brochure(*args,**kwargs):
    brochure = Brochure.objects.filter(show_on_site=True).all()
    if len(brochure)>0:
        return {
            'url':brochure[0].brochure.url,
            'title':brochure[0].title
        }
    else:
        return {}

def get_site_text(*args,**kwargs):
    alltexts = SiteText.objects.all()
    return { item.field_name:item.text for item in alltexts }

from lead.models import Lead
class IndexView(BaseAPIView):
    template_name = "shared/index.html"
    related_views = {
        'testimonials' : (TestimonialView.as_data(),'limit=5'),
        'homepagebanner':( HomePageBannerView.as_data(),'limit=5'),
        'homepagevideo':( HomePageVideoView.as_data(),'limit=5'),
        'leadchoices': (lambda *args,**kwargs: Lead.get_choices(),),
        'brochure':(get_brochure,)
    }

    
class AboutView(BaseAPIView):
    template_name = "shared/about.html"
    related_views = {
        'testimonials' : (TestimonialView.as_data(),'limit=2'),
        'messages': (MessageView.as_data(),)
    }

class PolicyView(BaseAPIView):
    template_name = "shared/policy.html"    

class ContactView(BaseAPIView):
    template_name = "shared/contact.html"
    related_views = {
        'leadchoices': (lambda *args,**kwargs: Lead.get_choices(),)
    }

from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
class CareerView(GenericAPIView,BaseAPIView):
    template_name = "shared/career.html"
    serializer_class = CareerSerializer
    parser_classes = (FormParser,MultiPartParser,JSONParser)
    related_views = {
        #'leadchoices': (lambda *args,**kwargs: Lead.get_choices(),)
    }
    def get(self,request,*args,**kwargs):
        response = super(CareerView,self).get(request,*args,**kwargs)
        response.data['success_message'] = kwargs.get('success',False)
        return response

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        if serializer.is_valid():
            serializer.save()
            kwargs['success']= True
        return self.get(request,*args,**kwargs)

from service.views import ServiceListView
class WhyView(BaseAPIView):
    template_name = "shared/why.html"
    related_views = {
        'services': (ServiceListView.as_data(),),
    }

from product.views import ProductListView
from itertools import groupby
class HeaderView(mixins.APIView):
    related_views = {
        'products': (ProductListView.as_data(),'limit=50'),
        'services': (ServiceListView.as_data(),'limit=20'),
        'texts':( get_site_text,)
    }
    def get_final_response(self,request,response):
        products = response.data.get("products",{})
        if products:
            response.data["product_group"]= [(key,[val for val in group]) for key,group in groupby(products["results"],lambda x:x["category"])]
        else:
            response.data["product_group"]= []
        return response
