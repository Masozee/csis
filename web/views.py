from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def Acara(request):
    acara = Event.objects.filter(publish=True).order_by('date_start').distinct()
    paginator = Paginator(acara, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        acara = paginator.page(page)
    except PageNotAnInteger:
        acara = paginator.page(1)
    except EmptyPage:
        acara = paginator.page(paginator.num_pages)
    
    return render(request, "web/events.html", {"acara":acara})

def AcaraDetail(request, Event_slug):
    acara = Event.objects.get(slug=Event_slug)
    
    context = {
        "acara": acara,
        
    }
    return render(request, "web/event-detail.html", context)


def DepartmentDetail(request, Department_slug):
    dept = Department.objects.get(slug=Department_slug)
    publication = Publication.objects.filter( department = dept.id)
    scholars = Person.objects.filter( department = dept.id)
    acara = Event.objects.filter( department = dept.id)

    context = {
        "Dept": dept,
        "publication": publication,
        "Scholars": scholars,
        "acara": acara,
    }
    return render(request, "web/department.html", context)


def Publications(request):
    publication = Publication.objects.filter(publish=True).order_by('date_created').distinct()
    paginator = Paginator(publication, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        publications = paginator.page(1)
    except EmptyPage:
        publications = paginator.page(paginator.num_pages)
    
    return render(request, "web/publications.html", {"publications":publications})

def PublicationDetail(request, Publication_slug):
    publication = Publication.objects.get(slug=Publication_slug)
    
    context = {
        "publications": publication,
        
    }
    return render(request, "web/publication-detail.html", context)