from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page_not_found_view(request, exception):
    return render(request, 'web/404.html', status=404)


# Create your views here.
def home(request):
   
    print = Publication.objects.filter(publish=True, highlight=True).order_by('-date_publish').distinct()[:1]
    small_pub = Publication.objects.filter(publish=True).order_by('-date_publish').distinct()[:3]
    acara = Event.objects.filter(publish=True).order_by('-date_created').distinct()[:5]
    project = Project.objects.filter(publish=True).order_by('-date_created').distinct()[:2]
    
    context = {
        
        'print': print,
        'smallpub': small_pub,
        'Acara': acara,
        'Project': project
       
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
    post_related = publication.tags.similar_objects()[:5]
    post_recent = Publication.objects.all().order_by('date_created').distinct()[:5]
    
    context = {
        "publications": publication,
        "post_related": post_related,
        "post_recent": post_recent,
        
    }
    return render(request, "web/publication-detail.html", context)

def PublicationCategoryDetail(request, Publication_category_slug):

    publication = Publication.objects.filter(publish=True, category__slug = Publication_category_slug).order_by('date_created').distinct()
    return render(request, "web/publications.html", {"publications":publication})

def Projects(request):
    projects = Project.objects.filter(publish=True).order_by('date_created').distinct()
    paginator = Paginator(projects, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    return render(request, "web/project.html", {"projects":projects})

def ProjectDetail(request, Project_slug):
    projects = Project.objects.get(slug=Project_slug)
    publication = Publication.objects.filter( project = projects.id)
    acara = Event.objects.filter( project = projects.id)

    
    context = {
        "projects": projects,
        "publication": publication,
        "acara": acara,
        
    }
    return render(request, "web/project-detail.html", context)

def news(request):
    newslist = News.objects.filter(publish=True).order_by('date_created').distinct()
    paginator = Paginator(newslist, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        newslist = paginator.page(page)
    except PageNotAnInteger:
        newslist = paginator.page(1)
    except EmptyPage:
        newslist = paginator.page(paginator.num_pages)
    
    return render(request, "web/news.html", {"newslist":newslist})

def newsDetail(request, News_slug):
    news = News.objects.get(slug=News_slug)
    post_related = news.tags.similar_objects()[:5]
    post_recent = News.objects.all().order_by('date_created').distinct()[:5]
    
    context = {
        "newslist": news,
        "post_related": post_related,
        "post_recent": post_recent,
        
    }
    return render(request, "web/news-detail.html", context)