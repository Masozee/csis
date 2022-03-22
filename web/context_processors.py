from .models import Department, Publication, Publication_category


def menu(request):
    recent_publication = Publication.objects.filter(publish=True).order_by('date_created')[:1]
    menu_publication = Publication.objects.filter(publish=True).order_by('-date_created')[:8]
    menu_dept = Department.objects.filter(publish=True)
    menu_cat = Publication_category.objects.all()


    context = {
        "menu_pub": menu_publication,
        "menu_dep":menu_dept,
        "cat": menu_cat,
        "recent_pub": recent_publication,

    }
    return context
   