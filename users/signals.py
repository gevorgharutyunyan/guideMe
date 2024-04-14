from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialLogin
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    """
    Signal receiver that executes after a user has signed up.
    We check if the signup is via a social account and mark the user as new.
    """
    # Check if the signup is via social account
    if isinstance(kwargs.get('sociallogin'), SocialLogin):
        # Mark the user session as a new social user
        request.session['is_new_social_user'] = True

# Ensure signals.py is imported in apps.py or similar to be active
