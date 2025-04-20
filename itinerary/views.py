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


HERE_API_KEY = settings.HERE_API_KEY

@login_required
def fetch_recommended_places(request, trip_id):
    try:
        itinerary = Itineraries.objects.get(id=trip_id, user=request.user)
    except Itineraries.DoesNotExist:
        return JsonResponse({"error": "Itinerary not found"}, status=404)

    latitude = 13.7563  # Bangkok
    longitude = 100.5018  # Bangkok
    radius = 2000  # Search radius in meters
    api_key = HERE_API_KEY

    url = f"https://discover.search.hereapi.com/v1/discover"
    params = {
        "apiKey": api_key,
        "at": f"{latitude},{longitude}",
        "q": "restaurants",
        "limit": 20,
        "lang": "en",
        "categories": "100-1000-0001"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Debugging response
    print("HERE API RESPONSE:", data)

    attractions = [
        {
            "name": place["title"],
            "lat": place["position"]["lat"],
            "lng": place["position"]["lng"]
        }
        for place in data.get("items", [])
    ]

    return JsonResponse({"tourist_attractions": attractions})


def edit_itinerary(request, trip_id):
    itinerary = Itineraries.objects.get(id=trip_id, user=request.user)
    return render(request, 'itinerary/edit_itinerary.html', {"itinerary": itinerary})

