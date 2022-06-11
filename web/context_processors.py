from .models import Department, Publication, Publication_category, Topic, Person


def menu(request):
    recent_publication = Publication.objects.filter(publish=True).order_by('-date_publish')[:1]
    menu_publication = Publication.objects.filter(publish=True).order_by('-date_publish')[:5]
    menu_dept = Department.objects.filter(publish=True)
    menu_cat = Publication_category.objects.all().order_by('name')
    menu_commentaries = Publication.objects.filter(category=1)[:4]
    menu_covid = Publication.objects.filter(category=3)[:3]
    menu_policy_brief = Publication.objects.filter(category=2)[:7]
    menu_experts = Topic.objects.filter(publish=True).order_by('-name')
    people_experts = Person.objects.filter(highlight=True)[:2]


    context = {
        "menu_pub": menu_publication,
        "menu_dep":menu_dept,
        "cat": menu_cat,
        "recent_pub": recent_publication,
        "menu_commentaries": menu_commentaries,
        "menu_covid": menu_covid,
        "menu_policy_brief": menu_policy_brief,
        "menu_experts": menu_experts,
        "people_experts": people_experts,

    }
    return context
   