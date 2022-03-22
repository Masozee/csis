from django.urls import path, include, re_path
from django.views.generic import TemplateView
from web import views as webviews

urlpatterns = [
    path('', webviews.home, name='home'),
    path('scholars/', webviews.Scholars, name='researcher'),
    re_path('scholar/(?P<Person_slug>[\w-]+)/$', webviews.ScholarDetail, name='researcher-detail'),
    path('publications/', webviews.Publications, name='publication'),
    re_path('publication/(?P<Publication_slug>[\w-]+)/$', webviews.PublicationDetail, name='publication-detail'),
    path('events/', webviews.Acara, name='event'),
    re_path('event/(?P<Event_slug>[\w-]+)/$', webviews.AcaraDetail, name='event-detail'),
    path('projects/', TemplateView.as_view(template_name='web/project.html'), name='project'),
    path('project/detail', TemplateView.as_view(template_name='web/project-detail.html'), name='project-detail'),
    path('news/', TemplateView.as_view(template_name='web/news.html'), name='news'),
    path('news/detail', TemplateView.as_view(template_name='web/news-detail.html'), name='news-detail'),
    path('faq/', TemplateView.as_view(template_name='web/faq.html'), name='faq'),
    path('privacy-policy/', TemplateView.as_view(template_name='web/home-grid.html'), name='privacy-policy'),
    path('about-us/', TemplateView.as_view(template_name='web/about.html'), name='about'),
    path('internship-and-fellowship/', TemplateView.as_view(template_name='web/home-grid.html'), name='intern'),
    re_path('department/(?P<Department_slug>[\w-]+)/$', webviews.DepartmentDetail, name='dept-detail'),
]   