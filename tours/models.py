
from django.db import models
from users.models import UserProfile
from django.conf import settings

DIFFICULTY_LEVELS=(('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard'))
LANGUAGES=(('ENG', 'English'), ('ARM', 'Armenian'), ('RUS', 'Russian'))
TOUR_STATUS = (('available', 'Available'), ('full', 'Full'), ('cancelled', 'Cancelled'))

class Tour(models.Model):
    guide = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=200, blank=True)
    max_group_size = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of participants")
    minimum_age = models.PositiveIntegerField(null=True, blank=True, help_text="Minimum age required to join the tour")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, blank=True,
                                        help_text="Difficulty level of the tour")
    languages = models.CharField(max_length=20, choices=LANGUAGES,blank=True, help_text="Languages in which the tour is offered")
    status = models.CharField(max_length=20, choices=TOUR_STATUS, default='available',
                              help_text="Current status of the tour")
    category = models.CharField(max_length=100, blank=True, help_text="Category of the tour")
    meeting_point = models.CharField(max_length=255, blank=True, help_text="Meeting point for the start of the tour")

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
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
    rating_overall = models.PositiveIntegerField(blank=True, null=True,help_text="Overall tour rating")
    rating_guide = models.PositiveIntegerField(blank=True, null=True,
                                               help_text="Rating for the guide's knowledge and professionalism")
    rating_value = models.PositiveIntegerField(blank=True, null=True, help_text="Value for money rating")
    rating_equipment = models.PositiveIntegerField(blank=True, null=True, help_text="Rating for the equipment provided")
    response = models.TextField(blank=True, help_text="Tour operator's response")
    response_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, help_text="Whether the review is from a verified participant")
    is_visible = models.BooleanField(default=True, help_text="If the review is visible to the public")

    def is_verified_participant(self):
        """Check if the author has a completed booking for the tour."""
        return Booking.objects.filter(tour=self.tour, user=self.author.profile, status='completed').exists()

    def __str__(self):
        return f'Review by {self.author.username} for {self.tour.title}'

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)