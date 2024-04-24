
from django.db import models
from users.models import UserProfile
from django.conf import settings
class Tour(models.Model):
    guide = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    duration = models.PositiveIntegerField(blank=True,help_text="Duration in hours")
    availability_start = models.DateField(null=True, blank=True,)
    availability_end = models.DateField(null=True, blank=True,)
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude for the tour location")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude for the tour location")
    location = models.CharField(max_length=255, blank=False, null=True, help_text="Human-readable location name")


    def __str__(self):
        return self.title

class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tour_images/', null=True, blank=True)

    def __str__(self):
        return f"Images for {self.tour.title}"

class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tour.title} by {self.user.user.username} on {self.booking_date}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tour_reviews')
    rating = models.PositiveIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.author.username} for {self.tour.title}'
