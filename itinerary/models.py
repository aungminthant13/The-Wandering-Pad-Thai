# from django.conf import settings
# from django.db import models

# class Itineraries(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     start_date = models.DateField(null=True, blank=True)
#     return_date = models.DateField(null=True, blank=True)
#     duration = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

from django.conf import settings
from django.db import models

class Itineraries(models.Model):
    """Main itinerary/trip model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    return_date = models.DateField()
    
    # Optional fields
    destination_city = models.CharField(max_length=100, default='Bangkok')
    destination_country = models.CharField(max_length=100, default='Thailand')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['user', '-start_date']),
        ]
        verbose_name_plural = "Itineraries"  # Keep the plural form in admin
    
    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.return_date})"
    
    @property
    def duration(self):
        """Calculate duration dynamically"""
        if self.start_date and self.return_date:
            return (self.return_date - self.start_date).days + 1
        return 0


class PlaceCards(models.Model):
    """Individual place/activity in the itinerary"""
    itinerary = models.ForeignKey(Itineraries, on_delete=models.CASCADE, related_name='place_cards')
    
    # Core fields
    title = models.CharField(max_length=200)  # Changed from place_name to title
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Google Places data
    google_place_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    google_place_name = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Order within the day
    order = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'order', 'start_time']
        indexes = [
            models.Index(fields=['itinerary', 'date', 'order']),
            models.Index(fields=['google_place_id']),
        ]
        unique_together = [['itinerary', 'date', 'order']]
        verbose_name_plural = "Place Cards"
    
    def __str__(self):
        time_str = f" at {self.start_time}" if self.start_time else ""
        return f"{self.title}{time_str} on {self.date}"
