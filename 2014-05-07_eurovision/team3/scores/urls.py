from django.conf.urls import *

from django.conf.urls import url, patterns, include
from rest_framework import viewsets, routers, serializers, filters
from models import Country, CountryScore


urlpatterns = patterns('scores.views',
        (r'^dumps/$', 'dumps'),
)


# rest framework setup

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    total_score = serializers.Field()

    class Meta:
        model = Country
        fields = ('name', 'total_score')

class CountryViewSet(viewsets.ModelViewSet):
    model = Country
    serializer_class = CountrySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', )

class ScoreViewSet(viewsets.ModelViewSet):
    model = CountryScore
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('score', )

router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'countryscore', ScoreViewSet)

urlpatterns += patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)