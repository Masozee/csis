from django.urls import path, include, re_path
from django.views.generic import TemplateView
from apps.dashboard import views as dashviews


urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard/index.html"), name='dashhome'),
    path('person/details', TemplateView.as_view(template_name="dashboard/user-profile.html"), name='profile-detail'),
    path('person/', TemplateView.as_view(template_name="dashboard/user-list.html"), name='profile'),
    path('publications/', TemplateView.as_view(template_name="dashboard/publication/publication.html"), name='publication'),

]