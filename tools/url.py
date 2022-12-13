from django.urls import path, include, re_path
from django.views.generic import TemplateView
from tools import views as toolsviews

from .models import *

urlpatterns = [
    
   
    re_path('S/Test/', toolsviews.redirect_view, name='redirect'),
    
]   