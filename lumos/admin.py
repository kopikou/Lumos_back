from django.contrib import admin
from lumos.models import *

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','phone','balance'] 

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','show_type']      

@admin.register(ShowRate)
class ShowRateAdmin(admin.ModelAdmin):
    list_display = ['id','show_type','rate']      

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['id','title','duration','cost','type','cnt_artists']   

@admin.register(ArtistPerformance)
class ArtistPerformanceAdmin(admin.ModelAdmin):
    list_display = ['artist','performance','rate']   

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','date','location','performance','amount','comment','completed']   

@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ['order','artist','amount','paid']   
