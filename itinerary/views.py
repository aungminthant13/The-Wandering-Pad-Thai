from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Itineraries
from .forms import CreateItineraryForm

@login_required
def create_itin(request):
    if request.method == 'POST':
        form = CreateItineraryForm(request.POST)
        if form.is_valid():
            # Save the itinerary with the current user
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.save()
            return redirect('itinerary:create_main_itin')  # Use namespace 'itinerary'

    else:
        form = CreateItineraryForm()

    return render(request, 'itinerary/create_itin.html', {'form': form})

@login_required
def create_main_itin(request):
    return render(request, 'itinerary/create_main_itin.html')