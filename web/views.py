from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
   
    print = Publication.objects.filter(publish=True).order_by('-date_created').distinct()[:3]
    acara = Event.objects.filter(publish=True).order_by('-date_created').distinct()[:6]
    
    context = {
        
        'print': print,
        'Acara': acara,
       
    }
    return render(request, "web/index.html", context)