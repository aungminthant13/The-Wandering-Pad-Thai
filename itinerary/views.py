from django.shortcuts import render
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from .models import Itineraries


@login_required
@csrf_exempt
def create_itinerary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get data from request
            trip_title = data.get('trip_title', 'Untitled Trip')
            start_date = data.get('start_date')
            return_date = data.get('return_date')
            
            # Create the itinerary
            itinerary = Itineraries.objects.create(
                user=request.user,
                title=trip_title,
                start_date=start_date,
                return_date=return_date,
                # Duration is now a calculated property, so we don't need to save it
            )
            
            return JsonResponse({
                'success': True,
                'itinerary_id': itinerary.id,
                'message': 'Itinerary created successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error creating itinerary: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


def edit_itinerary(request, itinerary_id):
    itinerary = Itineraries.objects.get(id=itinerary_id, user=request.user)
    start = itinerary.start_date
    duration = itinerary.duration
    date_list = [start + timedelta(days=i) for i in range(duration)]
    
    return render(request, 'itinerary/edit_itinerary.html', {
        "itinerary": itinerary,
        "date_list": date_list,
        })
