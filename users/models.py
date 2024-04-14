from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_tourist = models.BooleanField(default=False)
    is_guide = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)  # For guides
    rating = models.FloatField(default=0.0)  # For guides
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    def profile_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.STATIC_URL + 'img/user.png'


    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create or update user profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
