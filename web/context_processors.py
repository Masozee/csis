from .models import Publication 


def menu(request):
    menu = Publication.objects.all()
    return {'menu': menu}