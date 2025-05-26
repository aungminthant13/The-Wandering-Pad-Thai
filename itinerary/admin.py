from django.contrib import admin

# Register your models here.
from .models import Itineraries, PlaceCards

class PlaceCardsInline(admin.TabularInline):
    model = PlaceCards
    extra = 0
    fields = ['date', 'order', 'title', 'start_time', 'end_time', 'google_place_id']

@admin.register(Itineraries)
class ItinerariesAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_date', 'return_date', 'created_at']
    list_filter = ['start_date', 'destination_city']
    search_fields = ['title', 'user__email', 'user__name']
    inlines = [PlaceCardsInline]

@admin.register(PlaceCards)
class PlaceCardsAdmin(admin.ModelAdmin):
    list_display = ['title', 'itinerary', 'date', 'start_time', 'order']
    list_filter = ['date', 'itinerary__destination_city']
    search_fields = ['title', 'google_place_name', 'google_place_id']