from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itinerary.models import Itineraries


@login_required
def home(request):
    return render(request, 'home/index.html')


def trips(request):
    user_itineraries = Itineraries.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'home/trips.html', {'itineraries': user_itineraries})
