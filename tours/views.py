from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour, TourImage
from .forms import BookingForm, TourForm, TourImageFormSet
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.models import UserProfile
from .models import Booking
from django.http import HttpResponseForbidden
from .forms import ReviewForm
def tour_list(request):
    tours = Tour.objects.all()  # You can add filtering logic here
    user_boolean = request.user.profile.is_guide
    return render(request, 'tours/tour_list.html', {'tours': tours, 'user_boolean':user_boolean})

def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.user = request.user.profile  # Assuming you have a profile linked to your user
            booking.save()
            return redirect('tours:tour_list')  # Redirect to tour listing page or a confirmation page
    else:
        form = BookingForm()
    return render(request, 'tours/book_tour.html', {'form': form, 'tour': tour})


@login_required
def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        formset = TourImageFormSet(request.POST, request.FILES, queryset=TourImage.objects.none())
        if form.is_valid() and formset.is_valid():
            tour = form.save(commit=False)
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            tour.guide = user_profile  # Adjust according to your user relationship
            tour.save()
            formset.instance = tour
            formset.save()
            return redirect('tours:tour_list')
    else:
        form = TourForm()
        formset = TourImageFormSet(queryset=TourImage.objects.none())
    return render(request, 'tours/create_tour.html', {'form': form, 'formset': formset})


def guides_dashboard_view(request):
    # Ensure only guides can access this view
    if not request.user.profile.is_guide:
        return redirect('main:home')

    tours = Tour.objects.filter(guide=request.user.profile)
    # Example for fetching notifications, implement as needed
    notifications = []

    return render(request, 'tours/guides_dashboard.html', {
        'tours': tours,
        'notifications': notifications
    })

def discover_tours_view(request):
    # featured_tours = Tour.objects.filter(is_featured=True)  # Example attribute
    tours = Tour.objects.all()
    return render(request, 'tours/discover_tours.html', { 'tours': tours}) #'featured_tours': featured_tours,


def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        formset = TourImageFormSet(request.POST, request.FILES, instance=tour)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()  # Save the formset to handle the images
            return redirect('tours:tour_list')  # Redirect to the tour list or dashboard
    else:
        form = TourForm(instance=tour)
        formset = TourImageFormSet(instance=tour)  # Initialize the formset with the current tour instance
    return render(request, 'tours/edit_tour.html', {'form': form, 'formset': formset})




@login_required
@require_POST  # Ensure this view can only be accessed via POST
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.user.profile.is_guide and tour.guide == request.user.profile:
        tour.delete()
        return redirect('tours:tour_list')
    else:
        # Handle unauthorized attempt
        return HttpResponseForbidden('You are not authorized to delete this tour.')
def view_bookings_in_profile(request):
    booked_tours = request.user.profile.bookings.all()
    return render(request, 'tours/booked_tours_in_profile.html', {'booked_tours': booked_tours})

def guide_profile_bookings(request):
    my_tours = request.user.profile.tours.all()
    return render(request, 'tours/guide_profile_template.html', {'my_tours': my_tours})


@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.author = request.user
            review.save()
            return redirect('tours:discover')  # Redirect to the tour detail page
    else:
        form = ReviewForm()
    return render(request, 'tours/add_review.html', {'form': form, 'tour': tour})