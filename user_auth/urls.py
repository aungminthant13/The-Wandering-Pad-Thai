from django.urls import path, include
from .views import signup_view, login_view, user_logout

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
]
