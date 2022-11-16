from django.conf.urls import include, url
from .views import LeadSaveView

urlpatterns = [
    url('^lead/create/$',LeadSaveView.as_view(),name="create_lead"),
]

