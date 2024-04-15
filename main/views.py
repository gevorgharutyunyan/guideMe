from django.shortcuts import redirect, render
from django.shortcuts import render
from users.models import UserProfile
import logging
logger = logging.getLogger(__name__)

def home_view(request):
    if not request.GET.get('ignore_role'):
        if request.session.pop('is_new_social_user', None):
            return redirect('users:choose_role')

        if request.user.is_authenticated:
            try:
                if request.user.profile.is_tourist:
                    return redirect('tours:discover')
                elif request.user.profile.is_guide:
                    return redirect('tours:guides_dashboard')
            except UserProfile.DoesNotExist:
                return redirect('users:choose_role')

    print("Rendering home page")
    return render(request, 'main/home.html')
