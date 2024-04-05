# tours/forms.py
from django.forms.widgets import DateInput
from django import forms
from .models import Booking, Tour
from .models import Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date']
        widgets = {
            'booking_date': DateInput(attrs={'type': 'date'})
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'price', 'duration', 'availability_start', 'availability_end']
        widgets = {
            'availability_start': DateInput(attrs={'type': 'date'}),
            'availability_end': DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']