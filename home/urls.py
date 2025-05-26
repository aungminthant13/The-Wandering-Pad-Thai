from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trips, name='trips'),
]

# from django.urls import path
# from .views import home

# urlpatterns = [
#     path('', home, name='home'),
# ]
