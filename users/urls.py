app_name = 'users'
from django.urls import path
from . import views



urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('choose_user_type/', views.choose_user_type, name='choose_user_type'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]