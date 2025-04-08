from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from lumos.models import *
from lumos.serializers import * 

class ArtistsViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class TypesViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class ShowRatesViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = ShowRate.objects.all()
    serializer_class = ShowRateSerializer

class PerformancesViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

class ArtistPerformancesViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = ArtistPerformance.objects.all()
    serializer_class = ArtistPerformanceSerializer

class OrdersViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class EarningsViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Earning.objects.all()
    serializer_class = EarningSerializer
