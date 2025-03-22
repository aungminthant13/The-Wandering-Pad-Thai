from django.conf import settings
from django.db import models

class Itineraries(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
