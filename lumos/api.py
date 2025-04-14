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
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return ShowRateCreateUpdateSerializer
        return super().get_serializer_class()

class PerformancesViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return PerformanceCreateUpdateSerializer
        return super().get_serializer_class()

class ArtistPerformancesViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = ArtistPerformance.objects.all()
    serializer_class = ArtistPerformanceSerializer
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return ArtistPerformanceCreateUpdateSerializer
        return super().get_serializer_class()

class OrdersViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return OrderCreateUpdateSerializer
        return super().get_serializer_class()

class EarningsViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Earning.objects.all()
    serializer_class = EarningSerializer
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return EarningCreateUpdateSerializer
        return super().get_serializer_class()
