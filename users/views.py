from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import UserProfile
from .forms import UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if the UserProfile already exists and get or create accordingly
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_tourist = form.cleaned_data.get('is_tourist', False)
            profile.is_guide = form.cleaned_data.get('is_guide', False)
            profile.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('users:login')  # Adjust the namespace and URL name as necessary
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.profile.is_guide:
            return reverse_lazy('tours:guides_dashboard')
        else:
            return reverse_lazy('tours:discover')  # Update with your actual URL name


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, *args, **kwargs):
        # Custom actions before logout, if needed
        return super().dispatch(*args, **kwargs)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:edit_profile')  # Or redirect to another page
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'users/edit_profile.html', {'form': form})