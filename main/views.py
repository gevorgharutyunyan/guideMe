# main/views.py

from django.shortcuts import render

def home_view(request):
    # You can include any logic here for things you want to send to the template
    return render(request, 'main/welcome_page.html')
