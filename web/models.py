from distutils.command.upload import upload
from tokenize import blank_re
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from requests import request
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.utils.timezone import now
from embed_video.fields  import  EmbedVideoField
from datetime import date
from django.conf import settings
from django.db.models import Q
from django.template.defaultfilters import truncatechars
from django.core.validators import RegexValidator


# Create your models here.
phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")


class Department (models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(default='', editable=False, max_length=320)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'dept/', blank=True)
    image_credit = models.TextField(blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ("Department")
        verbose_name_plural = ("Departments")
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def events(self):
        return Event.objects.filter(department=self, publish=True).order_by('-date_start')[:7]

    @property
    def projects(self):
        return Project.objects.filter(department=self, publish=True)

    @property
    def peoples(self):
        return Person.objects.filter(department=self, is_active=True, category='Scholar').order_by('name')

    @property
    def publications(self):
        return Publication.objects.filter(department=self, publish=True).order_by('-date_publish')[:7]

class Topic(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default='', editable=False, max_length=320)
    description = RichTextField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to = 'Topic/', blank=True)
    image_credit = models.TextField(blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ("Reseach Topic")
        verbose_name_plural = ("Research Topic")
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    
    def main_topic(self):
        return self.objects.all(parent__isNull=True)

    def sub_topic(self):
        return self.topic_set.select_related('parent')

    @property
    def events(self):
        return Event.objects.filter(topic=self, publish=True).order_by('-date_start')[:7]

    @property
    def projects(self):
        return Project.objects.filter(project_topic=self, publish=True)

    @property
    def peoples(self):
        return Person.objects.filter(expertise=self, is_active=True, category='Scholar').order_by('name')

    @property
    def publications(self):
        return Publication.objects.filter(topic=self, publish=True).order_by('-date_publish')[:7]

class Person (models.Model):
    KATEGORI_CHOICES = (
        ('Scholar', 'Scholar'),
        ('Staff', 'Staff'),
        ('Foundation', 'Foundation'),
        ('Speaker', 'Speaker'),
        ('Colleague', 'Colleague'),
        ('Partner', 'Partner'),

    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(default='', editable=False, max_length=160)
    photo = models.ImageField(upload_to = 'person/', blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    organization = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    expertise = models.ManyToManyField(Topic, blank=True)
    department = models.ManyToManyField(Department, blank=True)
    is_active = models.BooleanField()
    description = RichTextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    highlight = models.BooleanField(default=False)
    order = models.PositiveIntegerField(blank=True,null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True, null=True, blank=True)
    contactPerson = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    external_profile = models.URLField(default='#', blank=True, null=True)


    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = ("Network")
        verbose_name_plural = ("Networks")
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def events(self):
        return Event.objects.filter(topic=self, publish=True).order_by('-date_start')[:7]

    @property
    def publications(self):
        return Publication.objects.filter(topic=self, publish=True).order_by('-date_publish')[:7]

    @property
    def profile_url(self):
        if self.category == 'Scholar':
            return f'/scholar/{self.slug}'
        return self.external_profile

    @property
    def profile_img(self):
        if self.photo:
            return f'https://s3-csis-web.s3.ap-southeast-1.amazonaws.com/{self.photo}'
        return f'https://s3-csis-web.s3.ap-southeast-1.amazonaws.com/static/web/avatar.png'

class TaggedProject(TaggedItemBase):
    content_object = models.ForeignKey('Project', on_delete=models.CASCADE)

class Project(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=160)
    department = models.ManyToManyField(Department, blank=True)
    partner = models.ManyToManyField(Person, blank=True,related_name="Project_Partner", limit_choices_to={'category': "Partner"})
    project_member = models.ManyToManyField(Person)
    project_topic = models.ManyToManyField(Topic, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to = 'project/', help_text="max height 1280px")
    periode_start = models.DateField(blank=True, null=True)
    periode_end = models.DateField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager(through=TaggedProject, blank=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("Project")
        verbose_name_plural = ("Projects")
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def short_title(self):
        return truncatechars(self.title, 35)


class Publication_category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(default='', editable=False, max_length=200)
    background = models.ImageField(upload_to = 'pub_category/', blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ("Publication Category")
        verbose_name_plural = ("Publication Categories")

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class TaggedPublication(TaggedItemBase):
    content_object = models.ForeignKey('Publication', on_delete=models.CASCADE)

class Publication(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=320)
    date_publish = models.DateField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    authors = models.ManyToManyField(Person)
    editor = models.ManyToManyField(Person, blank=True, related_name="publications_editor")
    category = models.ForeignKey(Publication_category, on_delete=models.CASCADE, blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL)
    topic = models.ManyToManyField(Topic, blank=True)
    department = models.ManyToManyField(Department, blank=True)
    partners = models.ManyToManyField(Person, blank=True,related_name="Publication_Partner", limit_choices_to={'category': "Partner"})
    image = models.ImageField(upload_to = 'publication/')
    image_credit = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to = 'publication/cover/', blank=True, null=True)
    file = models.FileField(upload_to='doc/', blank=True)
    description = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    highlight = models.BooleanField(default=False)
    tags = TaggableManager(through=TaggedPublication, blank=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("Publication")
        verbose_name_plural = ("Publications")
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


    
    @property
    def tgl(self):
        return self.date_created.strftime('%d %B %Y')
    
    def credit(self):
        return "Credit image : "+" "+self.image_credit

    @property
    def partner(self):
        # Check if self.project is not None
        if self.project is not None:
            # Use the getattr() function to safely access the partner attribute
            partners = getattr(self.project, "partner", None)
        else:
            partners = None

        return partners

class TaggedEvent(TaggedItemBase):
    content_object = models.ForeignKey('Event', on_delete=models.CASCADE)


class Event(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=320)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    Person_In_Charge = models.EmailField(blank=True, null=True)
    opening_speech = models.ManyToManyField(Person, related_name='OpeningSpeaker', blank=True)
    Moderator = models.ForeignKey(Person,on_delete=models.CASCADE, blank=True, null=True, related_name='Moderator')
    closing_remarks = models.ManyToManyField(Person, related_name='ClosingSpeaker', blank=True)
    speaker = models.ManyToManyField(Person, blank=True)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department, blank=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    topic = models.ManyToManyField(Topic, blank=True)
    image = models.ImageField(upload_to='event/img/')
    file = models.FileField(upload_to='event/file/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    youtube = EmbedVideoField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=TaggedEvent)
    publish = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("Event")
        verbose_name_plural = ("Events")
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    @property
    def tgl(self):
        return self.date_start.strftime('%d')+'-'+self.date_end.strftime('%d %B, %Y')

    def tgl_one_day(self):
        return self.date_start.strftime('%d %B, %Y')

    def tglselesai(self):
        return self.date_end.strftime('%d %B %Y')

    def is_past_due(self):
        return date.today() > self.date

    def waktu_mulai(self):
        return self.date_start.strftime('%H:%M')

    def waktu_selesai(self):
        return self.date_end.strftime('%H:%M')
    
    def waktu(self):
        return self.waktu_mulai.strftime('%H:%M') +" - "+ self.waktu_selesai.strftime('%H:%M')

    @property
    def partner(self):
        # Check if self.project is not None
        if self.project is not None:
            # Use the getattr() function to safely access the partner attribute
            partners = getattr(self.project, "partner", None)
        else:
            partners = None

        return partners

    @property
    def session(self):
        return EventSession.objects.filter(Events=self)

class TaggedNews(TaggedItemBase):
    content_object = models.ForeignKey('News', on_delete=models.CASCADE)

class News(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=160)
    date_release = models.DateField(default=now, blank=True, null=True)
    description = RichTextField()
    image = models.ImageField(upload_to = 'project/')
    image_credit = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager(through=TaggedNews)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("News")
        verbose_name_plural = ("News")
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Foundation(models.Model):
    Title = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=160)
    member = models.ManyToManyField(Person, blank=True)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'project/', blank=True, null=True)
    publish = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Title
        
    class Meta:
        verbose_name = ("BOD/Foundations")
        verbose_name_plural = ("BOD/Foundations")
    
    def save(self, *args, **kwargs):
        value = self.Title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class ExternalPublications(models.Model):
    N = '0'
    P = '1'
    D = '2'

    KATEGORI_PAPER_CHOICES = (
        (N, 'News'),
        (P, 'Paper'),
        (D, 'Book'),
    )
    title = models.CharField(max_length=350)
    author = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'category': "Scholar"})
    link = models.URLField(blank=True,null=True)
    category = models.CharField(max_length=2, choices=KATEGORI_PAPER_CHOICES)
    source = models.CharField(max_length=50, blank=True, null=True)
    file = models.FileField(upload_to='externalpublications/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("External Publications")
        verbose_name_plural = ("External Publications")


class EventSession(models.Model):
    Title = models.CharField(max_length=150)
    Events = models.ForeignKey(Event, on_delete=models.CASCADE)
    Moderator = models.ForeignKey(Person, blank=True, null=True,  on_delete=models.CASCADE, related_name="session_moderator")
    Speakers = models.ManyToManyField(Person, blank=True)
    Time = models.DateField(blank=True, null=True)
    Start = models.TimeField(blank=True, null=True)
    End = models.TimeField(blank=True, null=True)
    Image = models.ImageField(upload_to = 'Event/session/')

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name = ("Events Session")
        verbose_name_plural = ("Events Sessions")

class SpeakerCategory(models.Model):
    Title = models.CharField(max_length=30)
    order = models.PositiveIntegerField()
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name = ("Speaker Category")
        verbose_name_plural = ("Speaker Categories")

class EventSpeaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(SpeakerCategory, on_delete=models.CASCADE)
    speakers = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        return self.event.title

    class Meta:
        verbose_name = ("Event's Speaker")
        verbose_name_plural = ("Event's Speakers")

