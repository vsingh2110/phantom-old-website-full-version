from relatedviews import mixins
from .models import Lead
from rest_framework.generics import CreateAPIView
from rest_framework import serializers

class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        exclude = ('created_date','modified_date','show_on_site',)

class LeadDataView(mixins.APIView):
    def get(self,request,*args,**kwargs):
        return Lead.get_choices()
    
class LeadSaveView(CreateAPIView):
    queryset = Lead.objects
    serializer_class = LeadCreateSerializer
