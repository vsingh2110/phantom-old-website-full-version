from django.shortcuts import render
import django_filters
from rest_framework import generics
from rest_framework.response import Response

from relatedviews import mixins

from relatedviews.rvutils import cstolist
from relatedviews.filters import MutableDjangoFilterBackend,OrderBackend,CountBackend,ListFilter
from relatedviews.pagination import NoPagination

from .models import Product,Feature,ProductFeatureRelation
from lead.models import Lead
from .serializers import ProductDetailSerializer,ProductListSerializer,FeatureSerializer

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('category',)

# Create your views here.

class ProductDetailView(mixins.RetrieveAPIView):
   queryset = Product.objects.filter(show_on_site=True).prefetch_related('feature_relation__feature')
   serializer_class = ProductDetailSerializer
   lookup_field = 'slug'

class ProductListView(mixins.ListAPIView):
    queryset = Product.objects.select_related('category').order_by('category','priority')
    serializer_class = ProductListSerializer
    filter_class = ProductFilter
    filter_backends = (MutableDjangoFilterBackend,CountBackend,)
    pagination_class = NoPagination

class FeatureListView(mixins.ListAPIView):
    queryset = Feature.objects
    serializer_class = FeatureSerializer
    pagination_class = NoPagination

from core.views import BaseAPIView 
class ProductView(BaseAPIView):
    template_name = "product/product-detail.html"
    related_views = {
        'product': (ProductDetailView.as_data(),'slug',),
        'related_products':(ProductListView.as_data(pagination_class=NoPagination),'limit=4'),
        'leadchoices': (lambda *args,**kwargs: Lead.get_choices(),)
    }

class CompareView(BaseAPIView):
    template_name = "product/comparison.html"
    def get(self,request,*args,**kwargs):
        ids= cstolist(request.query_params.get('ids',''))
        product_map={}
        all_features=[]
        if ids:
            products = Product.objects.filter(id__in=ids).values('name','slug','main_image','feature_relation__value','feature_relation__feature__name','feature_relation__feature__slug')
            feature_map = {}
            all_features = []
            product_map = {}
            for product in products:
                slug = product['slug']
                product_map[slug] =product_map.get(slug) or {}
                product_map[slug]['name']=product['name']
                product_map[slug]['slug']=product['slug']
                if product['feature_relation__feature__slug']:
                    if not feature_map.get(product['feature_relation__feature__slug'],False):
                        feature_map[product['feature_relation__feature__slug']] = True
                        all_features.append({'name':product['feature_relation__feature__name'],'slug':product['feature_relation__feature__slug']})
                    product_map[slug][product['feature_relation__feature__slug']]=product['feature_relation__value']
        res = {
            'features':all_features,
            'products':[value for slug,value in product_map.items()]
        }
        response = super(CompareView,self).get(request,*args,**kwargs)
        response.data.update(res)
        return response

