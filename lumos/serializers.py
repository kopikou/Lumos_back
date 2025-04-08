from rest_framework import serializers
from lumos.models import *

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "first_name", "last_name", "phone", "balance"]

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id','show_type']

class ShowRateSerializer(serializers.ModelSerializer):
    show_type = TypeSerializer(read_only=True)

    class Meta:
        model = ShowRate
        fields = ['id','show_type','rate'] 

class PerformanceSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = ['id','title','duration','cost','type','cnt_artists']   

class ArtistPerformanceSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    performance = PerformanceSerializer(read_only=True)
    rate = ShowRateSerializer(read_only=True)

    class Meta:
        model = ArtistPerformance
        fields = ['artist','performance','rate']  

class OrderSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id','date','location','performance','amount','comment','completed']  

class EarningSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Earning
        fields = ['order','artist','amount','paid'] 