from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Itineraries
# import json
# from django.http import JsonResponse
# import requests
from datetime import timedelta


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from .models import Itineraries


# @login_required
# def create_itinerary(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             trip_title = data.get("trip_title")
#             start_date = data.get("start_date")
#             return_date = data.get("return_date")
#             trip_duration = data.get("trip_duration")

#             if not (trip_title and start_date and return_date and isinstance(trip_duration, int)):
#                 return JsonResponse({"success": False, "message": "Missing or invalid fields"}, status=400)

#             itinerary = Itineraries.objects.create(
#                 user=request.user,
#                 title=trip_title,
#                 start_date=start_date,
#                 return_date=return_date,
#                 duration=trip_duration
#             )

#             return JsonResponse({"success": True, "itinerary_id": itinerary.id})

#         except json.JSONDecodeError:
#             return JsonResponse({"success": False, "message": "Invalid. Try Again!"}, status=400)

#     return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


# @login_required
# def recommended_places(request, itinerary_id):
#     itinerary = Itineraries.objects.get(id=itinerary_id, user=request.user)
#     return render(request, 'itinerary/recommended_places.html', {"itinerary": itinerary})

# MAPBOX_ACCESS_TOKEN = settings.MAPBOX_ACCESS_TOKEN

# @login_required
# def fetch_recommended_places(request, trip_id):
#     try:
#         itinerary = Itineraries.objects.get(id=trip_id, user=request.user)
#     except Itineraries.DoesNotExist:
#         return JsonResponse({"error": "Itinerary not found"}, status=404) 
    
#     latitude = 13.7563
#     longitude = 100.5018
    

# HERE_API_KEY = settings.HERE_API_KEY

# @login_required
# def fetch_recommended_places(request, trip_id):
#     try:
#         itinerary = Itineraries.objects.get(id=trip_id, user=request.user)
#     except Itineraries.DoesNotExist:
#         return JsonResponse({"error": "Itinerary not found"}, status=404)

#     latitude = 13.7563  # Bangkok
#     longitude = 100.5018  # Bangkok
#     radius = 20  # Search radius in meters
#     api_key = HERE_API_KEY

#     url = f"https://discover.search.hereapi.com/v1/discover"
#     params = {
#         "apiKey": api_key,
#         "at": f"{latitude},{longitude}",
#         "q": "restaurants",
#         "limit": 20,
#         "lang": "en",
#         "categories": "100-1000-0001"
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     # Debugging response
#     print("HERE API RESPONSE:", data)

#     attractions = [
#         {
#             "name": place["title"],
#             "lat": place["position"]["lat"],
#             "lng": place["position"]["lng"]
#         }
#         for place in data.get("items", [])
#     ]

#     return JsonResponse({"tourist_attractions": attractions})


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
