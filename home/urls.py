from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trips, name='trips'),
    path("auth/", include("user_auth.urls")),

]

# from django.urls import path
# from .views import home

# urlpatterns = [
#     path('', home, name='home'),
# ]
