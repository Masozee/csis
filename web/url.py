from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='web/index.html'), name='home'),
    path('researcher/', TemplateView.as_view(template_name='web/researcher.html'), name='researcher'),
    path('researcher/detail', TemplateView.as_view(template_name='web/researcher-detail.html'), name='researcher-detail'),
    path('publication/', TemplateView.as_view(template_name='web/publications.html'), name='publication'),
    path('publication/detail', TemplateView.as_view(template_name='web/publication-detail.html'), name='publication-detail'),
    path('events/', TemplateView.as_view(template_name='web/events.html'), name='event'),
    path('events/detail', TemplateView.as_view(template_name='web/event-detail.html'), name='event-detail'),
    path('project/', TemplateView.as_view(template_name='web/project.html'), name='project'),
    path('project/detail', TemplateView.as_view(template_name='web/project-detail.html'), name='project-detail'),
    path('news/', TemplateView.as_view(template_name='web/news.html'), name='news'),
    path('news/detail', TemplateView.as_view(template_name='web/news-detail.html'), name='news-detail'),
    path('faq/', TemplateView.as_view(template_name='web/faq.html'), name='faq'),
    path('privacy-policy/', TemplateView.as_view(template_name='web/home-grid.html'), name='privacy-policy'),
    path('about-us/', TemplateView.as_view(template_name='web/about.html'), name='about'),
    path('department/economics/', TemplateView.as_view(template_name='web/depekon.html'), name='depekon'),
    path('department/politics-and-social-changes/', TemplateView.as_view(template_name='web/deppol.html'), name='deppol'),
    path('department/international-relations/', TemplateView.as_view(template_name='web/dephi.html'), name='dephi'),
    path('internship-and-fellowship/', TemplateView.as_view(template_name='web/home-grid.html'), name='intern'),
]   