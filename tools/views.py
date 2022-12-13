from django.shortcuts import render

# views.py
from django.shortcuts import redirect

from .models import *

def redirect_view(request, Shorten_ShortenWord):
    direct = Shorten.objects.get(ShortenWord=Shorten_ShortenWord)
    
    return redirect("https://google.com")

