from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import UserProfile
from .forms import UserProfileForm


def choose_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.session['user_type'] = user_type  # Store the selection in the session
        return redirect('users:register')  # Redirect to the actual registration form

    return render(request, 'registration/user_type_selection.html')

def register(request):
    user_type = request.session.get('user_type', 'tourist')  # Default to 'tourist'
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            if user_type == 'tourist':
                profile.is_tourist = True
            else:
                profile.is_guide = True
            profile.save()
            del request.session['user_type']  # Clean up the session
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('users:login')
    else:
        form = UserRegisterForm(initial={'user_type': user_type})
    return render(request, 'registration/register.html', {'form': form})


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