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

def Scholars(request):
    scholar = Person.objects.filter(is_active=True).order_by('name').distinct()
    return render(request, "web/researcher.html", {"scholar":scholar})

def ScholarDetail(request, Person_slug):
    scholar = Person.objects.get(slug=Person_slug)
    publication = Publication.objects.filter( authors = scholar.id)
    

    context = {
        "scholar": scholar,
        "publication": publication,
    }
    return render(request, "web/researcher-detail.html", context)