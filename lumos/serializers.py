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
    show_type = TypeSerializer()

    class Meta:
        model = ShowRate
        fields = ['id','show_type','rate'] 
class ShowRateCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowRate
        fields = ['id','show_type','rate'] 

class PerformanceSerializer(serializers.ModelSerializer):
    type = TypeSerializer()

    class Meta:
        model = Performance
        fields = ['id','title','duration','cost','type','cnt_artists']   
class PerformanceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['id','title','duration','cost','type','cnt_artists']   

class ArtistPerformanceSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    performance = PerformanceSerializer(read_only=True)
    rate = ShowRateSerializer(read_only=True)

    class Meta:
        model = ArtistPerformance
        fields = ['id','artist','performance','rate']  
class ArtistPerformanceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistPerformance
        fields = ['id','artist','performance','rate']  

class OrderSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id','date','location','performance','amount','comment','completed']  
class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','date','location','performance','amount','comment','completed']  

class EarningSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Earning
        fields = ['id','order','artist','amount','paid'] 
class EarningCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earning
        fields = ['id','order','artist','amount','paid'] 


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Получаем группы пользователя
        is_admin = self.user.is_superuser  # или self.user.is_staff
        
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'is_admin': is_admin,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
     
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'is_admin', 'is_staff')
    
    def get_is_admin(self, obj):
        return obj.is_superuser or obj.groups.filter(name='Admin').exists()
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')