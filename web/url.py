from django.urls import path, include, re_path
from django.views.generic import TemplateView
from web import views as webviews

urlpatterns = [
    path('', webviews.home, name='home'),
    path('scholars/', webviews.Scholars, name='researcher'),
    re_path('scholar/(?P<Person_slug>[\w-]+)/$', webviews.ScholarDetail, name='researcher-detail'),
    path('publications/', webviews.Publications, name='publication'),
    re_path('publication/(?P<Publication_slug>[\w-]+)/$', webviews.PublicationDetail, name='publication-detail'),
    re_path('publications/(?P<Publication_category_slug>[\w-]+)/$', webviews.PublicationCategoryDetail, name='publicationcategory-detail'),
    path('events/', webviews.Acara, name='event'),
    re_path('event/(?P<Event_slug>[\w-]+)/$', webviews.AcaraDetail, name='event-detail'),
    path('projects/', webviews.Projects, name='project'),
    re_path('project/(?P<Project_slug>[\w-]+)/$', webviews.ProjectDetail, name='project-detail'),
    path('news/', webviews.news, name='news'),
    re_path('news/(?P<News_slug>[\w-]+)/$', webviews.newsDetail, name='news-detail'),
    path('research-topics/', webviews.topic, name='topic'),
    re_path('research-topic/(?P<Topic_slug>[\w-]+)/$', webviews.topicDetail, name='topic-detail'),
    path('faq/', TemplateView.as_view(template_name='web/faq.html'), name='faq'),
    path('privacy-policy/', TemplateView.as_view(template_name='web/home-grid.html'), name='privacy-policy'),
    path('about-us/', TemplateView.as_view(template_name='web/about.html'), name='about'),
    path('internship-and-fellowship/', TemplateView.as_view(template_name='web/home-grid.html'), name='intern'),
    re_path('department/(?P<Department_slug>[\w-]+)/$', webviews.DepartmentDetail, name='dept-detail'),
]   