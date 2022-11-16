from django.conf.urls import include, url
from .views import ServiceListBaseView

urlpatterns = [
    url('^services/$',ServiceListBaseView.as_view(),name="service_list"),
]


