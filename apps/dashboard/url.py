from django.urls import path, include, re_path
from django.views.generic import TemplateView
from apps.dashboard import views as dashviews


urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard/index.html"), name='dashhome'),

]