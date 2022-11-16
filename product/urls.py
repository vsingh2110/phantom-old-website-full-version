from django.conf.urls import include, url
from .views import ProductDetailView,ProductListView,ProductView,CompareView

urlpatterns = [
    url('^product/(?P<slug>[-\w]+)/$',ProductView.as_view(),name="product_detail"),
    url('^product/$',ProductListView.as_view(),name="product_list"),
    url('^compare-products/$',CompareView.as_view(),name="compare")
]
