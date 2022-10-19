from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from config.models import *
from .filters import publication_filter

def page_not_found_view(request, exception):
    return render(request, 'web/404.html', status=404)

def is_valid_query(param):
    return param != '' and param is not None
def filter(request):
    qs = Publication.objects.filter(publish=True).order_by('-date_publish').distinct()
    dept = Department.objects.filter(publish=True).order_by('-date_created').distinct()
    staff = Person.objects.all().order_by('-name')

    title_contains_query = request.GET.get('title_contains')
    dept_contains_query = request.GET.get('dept_contains')
    person_contains_query = request.GET.get('person_contains')

    if is_valid_query(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    if is_valid_query(dept_contains_query):
        qs = qs.filter(department__name__icontains=dept_contains_query)

    if is_valid_query(person_contains_query):
        qs = qs.filter(authors__name__icontains=person_contains_query)

    return qs

# Create your views here.
def home(request):
   
    print = Publication.objects.filter(publish=True, highlight=True).order_by('-date_publish').distinct()[:1]
    small_pub = Publication.objects.filter(publish=True).order_by('-date_publish').distinct()[:3]
    acara = Event.objects.filter(publish=True).order_by('-date_created').distinct()[:5]
    project = Project.objects.filter(publish=True).order_by('-date_created').distinct()[:2]
    slider = Slider.objects.filter(show=True).order_by('-date_created')
    
    context = {
        
        'print': print,
        'smallpub': small_pub,
        'Acara': acara,
        'Project': project,
        'slider': slider,
    }
    return render(request, "web/index.html", context)

def Scholars(request):
    scholar = Person.objects.filter(is_active=True, category="Scholar").order_by('name').distinct()
    return render(request, "web/researcher.html", {"scholar":scholar})

def ScholarDetail(request, Person_slug):
    scholar = Person.objects.get(slug=Person_slug)
    publication = Publication.objects.filter( authors = scholar.id).order_by('-date_publish')[:6]
    paginator = Paginator(publication, 9)

    page = request.GET.get('page')
    try:
        publication = paginator.page(page)
    except PageNotAnInteger:
        publication = paginator.page(1)
    except EmptyPage:
        publication = paginator.page(paginator.num_pages)
    
    context = {
        "scholar": scholar,
        "publication": publication,
    }
    return render(request, "web/researcher-detail.html", context)

def Acara(request):
    acara = Event.objects.filter(publish=True).order_by('-date_start').distinct()
    
    paginator = Paginator(acara, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        acara = paginator.page(page)
    except PageNotAnInteger:
        acara = paginator.page(1)
    except EmptyPage:
        acara = paginator.page(paginator.num_pages)

    context = {
        "acara": acara,
        
    }
    
    return render(request, "web/events.html", context)

def AcaraDetail(request, Event_slug):
    acara = Event.objects.get(slug=Event_slug)
    post_related = acara.tags.similar_objects()[:5]
    post_recent = Event.objects.all().order_by('date_created').distinct()[:5]

    context = {
        "acara": acara,
        "post_related": post_related,
        "post_recent": post_recent,
        
    }
    return render(request, "web/event-detail.html", context)

def DepartmentDetail(request, Department_slug):
    dept = Department.objects.get(slug=Department_slug)
    publication = Publication.objects.filter( department = dept.id)
    lead = Person.objects.filter( department = dept.id, order = 4, is_active=True)
    scholars = Person.objects.filter( department = dept.id, is_active=True).exclude( order = 4).order_by('-order')
    acara = Event.objects.filter( department = dept.id)

    context = {
        "Dept": dept,
        "publication": publication,
        "Scholars": scholars,
        "acara": acara,
        "lead":lead
    }
    return render(request, "web/department.html", context)

def Publications(request):
    publication = Publication.objects.filter(publish=True).order_by('-date_publish').distinct()
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
    pub = Publication_category.objects.get(slug=Publication_category_slug)
    publications_category = Publication.objects.filter(category=pub)

    context = {
       "publications" : publications_category,
       "pub": pub,
    }
    return render(request, "web/publications.html", context)

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

def topic(request):
    tplist = Topic.objects.filter(publish=True).order_by('date_created').distinct()
    paginator = Paginator(tplist, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        tplist = paginator.page(page)
    except PageNotAnInteger:
        tplist = paginator.page(1)
    except EmptyPage:
       tplist = paginator.page(paginator.num_pages)
    
    return render(request, "web/news.html", {"list":tplist})

def topicDetail(request, Topic_slug):
    news = Topic.objects.get(slug=Topic_slug)
    expert_related = news.person_set.all()
    article_related = news.publication_set.all()
    event_related = Event.objects.filter(topic=news).order_by('date_created')
    
    context = {
        "newslist": news,
        "expert_related": expert_related,
        "publications": article_related,
        "event_related": event_related,
        
    }
    return render(request, "web/research-category.html", context)

def bod(request):
    bod = Foundation.objects.filter(id=1).order_by("-member__order")[:1]

    return render(request, "web/bod.html", {"scholar":bod})

def yayasan(request):
    advisor = Foundation.objects.filter(id=2 ).order_by("-member__order")[:1]
    BoT = Foundation.objects.filter( id=3 ).order_by("-member__order")[:1]
    BoD = Foundation.objects.filter( id=4 ).order_by("-member__order")[:1]
    BoS = Foundation.objects.filter( id=5 ).order_by("-member__order")[:1]

    context = {
        "advisor": advisor,
        "BoT": BoT,
        "BoD": BoD,
        "BoS": BoS,
    }

    return render(request, "web/foundation.html", context)


#business logic yang ruwet-ruwet ada di sini

def handler_404(request):
    return render(request, "web/404.html")

def post_search(request):
    form = PostSearchForm()
    q = ''
    results = []

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']

            vector = SearchVector('title', weight='A') + SearchVector('authors__name', weight='C') + SearchVector('tags', weight='B')
            query = SearchQuery(q)

            results = Publication.objects.annotate(
                rank=SearchRank(vector, query, cover_density=True)).order_by('-rank').distinct()

    return render(request, 'web/search.html',
                  {'form': form,
                   'q': q,
                   'results': results})

def Publications_query(request):
    qs = filter(request)

    context = {
        'queryset': qs,
    }

    return render(request, "web/results.html", context)