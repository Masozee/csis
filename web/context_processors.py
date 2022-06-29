from .models import Department, Publication, Publication_category, Topic, Person


def menu(request):
    recent_publication = Publication.objects.filter(publish=True).order_by('-date_publish')[:1]
    menu_publication = Publication.objects.filter(publish=True).order_by('-date_publish')[:5]
    menu_dept = Department.objects.filter(publish=True)
    menu_cat = Publication_category.objects.all().order_by('name')
    menu_commentaries = Publication.objects.filter(category=3).order_by('-date_publish')[:4]
    menu_research_report = Publication.objects.filter(category=11).order_by('-date_publish')[:3]
    menu_policy_brief = Publication.objects.filter(category=2).order_by('-date_publish')[:7]
    menu_working_paper = Publication.objects.filter(category=12).order_by('-date_publish')[:2]
    menu_experts = Topic.objects.filter(publish=True).order_by('-name')
    people_experts = Person.objects.filter(highlight=True)[:2]


    context = {
        "menu_pub": menu_publication,
        "menu_dep":menu_dept,
        "cat": menu_cat,
        "recent_pub": recent_publication,
        "menu_commentaries": menu_commentaries,
        "menu_research_report": menu_research_report,
        "menu_policy_brief": menu_policy_brief,
        "menu_experts": menu_experts,
        "people_experts": people_experts,
        "menu_working_paper": menu_working_paper,

    }
    return context
   