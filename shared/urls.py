from django.conf.urls import include, url
from .views import IndexView,AboutView,WhyView,ContactView,CareerView, PolicyView

urlpatterns = [
    url('^$',IndexView.as_view(),name="index"),
    url('^about/$',AboutView.as_view(),name="about"),
    url('^why/$',WhyView.as_view(),name="why"),
    url('^contact/$',ContactView.as_view(),name="contact"),
    url('^careers/$',CareerView.as_view(),name="careers"),
    url('^privacy-policy/$',PolicyView.as_view(),name="policy"),
]

