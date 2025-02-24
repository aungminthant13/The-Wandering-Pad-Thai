from django.urls import path
from .views import create_itin, create_main_itin

app_name = 'itinerary'

urlpatterns = [
    path('create/', create_itin, name='create_itin'),
    path('create_itinerary/', create_main_itin, name='create_main_itin'),


]
