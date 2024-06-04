from django.urls import path
from . import views

app_name = 'tours'  # This allows for namespacing of your URLs

urlpatterns = [
    path('', views.tour_list, name='tours_list'),  # For listing tours
    path('guides_dashboard/', views.guides_dashboard_view, name='guides_dashboard'),
    path('discover/', views.discover_tours_view, name='discover'),
    path('edit/<int:tour_id>/', views.edit_tour, name='edit'),
    path('delete/<int:tour_id>/', views.delete_tour, name='delete'),
    path('tourist_bookings/', views.tourist_bookings_in_profile, name='tourist_bookings'),
    path('bookings_of_guide/', views.bookings_in_guide_profile, name='bookings_of_guide'),
    path('create/', views.create_tour, name='create'),
    path('<int:tour_id>/book/', views.book_tour, name='book_tour'),
    path('<int:tour_id>/add_review/', views.add_review, name='add_review'),# For booking a specific tour
    path('search_tours/', views.search_tours, name='search_tours'),

]