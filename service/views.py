from relatedviews import mixins
from relatedviews.pagination import NoPagination
from relatedviews.filters import MutableDjangoFilterBackend,OrderBackend,CountBackend

from .models import Service
from lead.models import Lead
from .serializers import ServiceListSerializer

class ServiceListView(mixins.ListAPIView):
    queryset = Service.objects.filter(show_on_site=True).order_by('priority')
    serializer_class = ServiceListSerializer
    filter_backends = (MutableDjangoFilterBackend,CountBackend,)
    pagination_class = NoPagination

from core.views import BaseAPIView 
class ServiceListBaseView(BaseAPIView):
    template_name = "service/service-list.html"
    related_views = {
        'services': (ServiceListView.as_data(),),
        'leadchoices': (lambda *args,**kwargs: Lead.get_choices(),)
    }
