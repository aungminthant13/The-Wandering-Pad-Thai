from django.urls import path
from .views import create_itinerary, recommended_places, fetch_recommended_places, edit_itinerary

app_name = 'itinerary'

urlpatterns = [
    path('create_itinerary/', create_itinerary, name='create_itinerary'),
    path('recommended_places/<int:trip_id>/', recommended_places, name='recommended_places'),
    path("trip/<int:trip_id>/recommended/api/", fetch_recommended_places, name="fetch_recommended_places"),

    path('edit/<int:trip_id>/', edit_itinerary, name='edit_itinerary'),
    # path('create_itinerary/', create_main_itin, name='create_main_itin'),
]
