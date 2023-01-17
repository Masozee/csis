from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
# views.py
from django.shortcuts import redirect

from .models import *

def redirect_view(request, Shorten_kategori, Shorten_ShortenWord):
    try:
        shortener = Shorten.objects.get(ShortenWord=Shorten_ShortenWord, kategori=Shorten_kategori)

        shortener.times_followed += 1

        shortener.save()

        return HttpResponseRedirect(shortener.Url)

    except:
        raise Http404('Sorry this link is broken :(')
