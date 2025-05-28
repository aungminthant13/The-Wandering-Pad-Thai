from django.urls import path
from .views import create_itinerary, edit_itinerary, save_itinerary
from . import views

app_name = 'itinerary'

urlpatterns = [
    path('create_itinerary/', create_itinerary, name='create_itinerary'),
    # path('', views.home, name='home'),;
    path('edit_itinerary/<int:itinerary_id>/', edit_itinerary, name='edit_itinerary'),
    path('save_itinerary/<int:itinerary_id>/', save_itinerary, name='save_itinerary'),

    #itineraray place card edit/ delete
    path('<int:itinerary_id>/place-cards/save/', views.save_place_card, name='save_place_card'),
    path('<int:itinerary_id>/place-cards/<int:card_id>/delete/', views.delete_place_card, name='delete_place_card'),
    path('<int:itinerary_id>/place-cards/update-order/', views.update_card_order, name='update_card_order'),
]
