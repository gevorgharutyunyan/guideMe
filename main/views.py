from django.shortcuts import redirect, render
from django.shortcuts import render
from users.models import UserProfile
from tours.models import Tour


def home_view(request):
    """
    Home view that checks user type and redirects accordingly.
    """
    if request.session.pop('is_new_social_user', None):
        # Redirect new users to role selection
        return redirect('users:choose_role')

    # Logic for determining where to redirect users based on their profile
    if request.user.is_authenticated:
        try:
            if request.user.profile.is_tourist:
                return redirect('tours:discover')
            elif request.user.profile.is_guide:
                return redirect('tours:guides_dashboard')
        except UserProfile.DoesNotExist:
            return redirect('users:choose_role')  # Redirect to choose role if profile does not exist

    tours = Tour.objects.all()  # Fetch all tour objects from the database
    return render(request, 'main/home.html', {'tours': tours})
