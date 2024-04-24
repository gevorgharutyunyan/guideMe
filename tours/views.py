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
    return render(request, 'tours/posted_tours_by_guides.html', {'tours': tours, 'user_boolean':user_boolean})

def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.user = request.user.profile  # Assuming you have a profile linked to your user
            booking.save()
            return redirect('tours:tourist_bookings')  # Redirect to tour listing page or a confirmation page
    else:
        form = BookingForm()
    return render(request, 'tours/book_tour.html', {'form': form, 'tour': tour})


@login_required
def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        formset = TourImageFormSet(request.POST, request.FILES)
        if form.is_valid():
            tour = form.save(commit=False)  # Save the form temporarily without committing to DB
            tour.guide = request.user.profile  # assuming you have a UserProfile related to your User
            latitude = request.POST.getlist('latitude')[0] if request.POST.getlist('latitude') else None
            longitude = request.POST.getlist('longitude')[0] if request.POST.getlist('longitude') else None


            # You need to set latitude and longitude on the tour object here
            if latitude and longitude:
                tour.latitude = float(latitude)
                tour.longitude = float(longitude)

            tour.save()
            formset = TourImageFormSet(request.POST, request.FILES, instance=tour)
            if formset.is_valid():
                formset.save()

            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

            images = request.FILES.getlist('images')
            for image in images:
                TourImage.objects.create(tour=tour, image=image)

            return redirect('tours:guides_dashboard')
    else:
        form = TourForm()
        formset = TourImageFormSet()

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


@login_required
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        formset = TourImageFormSet(request.POST, request.FILES, instance=tour)
        if form.is_valid() and formset.is_valid():
            updated_tour = form.save(commit=False)

            # Retrieve and convert latitude and longitude values before saving the Tour object
            try:
                updated_tour.latitude = float(request.POST.get('latitude', updated_tour.latitude))
                updated_tour.longitude = float(request.POST.get('longitude', updated_tour.longitude))
            except ValueError as e:
                pass

            # Saving the object after setting latitude and longitude
            updated_tour.save()
            print("Request Files before formset save:", request.FILES)
            formset.save()

            print("Form errors: before else", form.errors)
            print("Formset errors: before else", formset.errors)
            # Log the values that were supposed to be saved

            return redirect('tours:guides_dashboard')
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = TourForm(instance=tour)
        formset = TourImageFormSet(instance=tour)

    return render(request, 'tours/edit_tour.html', {'form': form, 'formset': formset})

@login_required
@require_POST  # Ensure this view can only be accessed via POST
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.user.profile.is_guide and tour.guide == request.user.profile:
        tour.delete()
        return redirect('tours:guides_dashboard')
    else:
        # Handle unauthorized attempt
        return HttpResponseForbidden('You are not authorized to delete this tour.')
def tourist_bookings_in_profile(request):
    booked_tours = request.user.profile.bookings.all()
    return render(request, 'tours/tourist_bookings_in_profile.html', {'booked_tours': booked_tours})

def bookings_in_guide_profile(request):
    my_tours = request.user.profile.tours.all()
    return render(request, 'tours/bookings_in_guide_profile.html', {'my_tours': my_tours})


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