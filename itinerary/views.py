from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Itineraries
import json
from django.http import JsonResponse
import requests
from django.conf import settings


@login_required
def create_itinerary(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            trip_title = data.get("trip_title")
            start_date = data.get("start_date")
            return_date = data.get("return_date")
            trip_duration = data.get("trip_duration")

            if not (trip_title and start_date and return_date and isinstance(trip_duration, int)):
                return JsonResponse({"success": False, "message": "Missing or invalid fields"}, status=400)

            itinerary = Itineraries.objects.create(
                user=request.user,
                title=trip_title,
                start_date=start_date,
                return_date=return_date,
                duration=trip_duration  # Save as integer
            )

            return JsonResponse({"success": True, "trip_id": itinerary.id})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@login_required
def recommended_places(request, trip_id):
    itinerary = Itineraries.objects.get(id=trip_id, user=request.user)
    return render(request, 'itinerary/recommended_places.html', {"itinerary": itinerary})


MAPQUEST_API_KEY = settings.MAPQUEST_API_KEY

@login_required
def fetch_recommended_places(request, trip_id):
    itinerary = Itineraries.objects.get(id=trip_id, user=request.user)

    latitude = 13.7563  # Bangkok
    longitude = 100.5018  # Bangkok

    url = "https://www.mapquestapi.com/search/v2/radius"
    params = {
        "key": MAPQUEST_API_KEY,
        "origin": f"{latitude},{longitude}",
        "radius": 200,
        "maxMatches": 20,
    }

    response = requests.get(url, params=params)
    data = response.json()

    #debug
    print("MAPQUEST RESPONSE:", data)

    attractions = [
        {
            "name": place["name"],
            "lat": place["fields"]["mqap_geography"]["latLng"]["lat"],
            "lng": place["fields"]["mqap_geography"]["latLng"]["lng"]
        }
        for place in data["searchResults"]
    ]


    return JsonResponse({"tourist_attractions": attractions})

