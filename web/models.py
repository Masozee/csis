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
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.conf import settings
from django.db.models import Q


# Create your models here.
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

class Person (models.Model):
    KATEGORI_CHOICES = (
        ('Scholar', 'Scholar'),
        ('Staff', 'Staff'),
        ('Foundation', 'Foundation'),
        ('Speaker', 'Speaker'),
        ('Colleague', 'Colleague')
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(default='', editable=False, max_length=160)
    photo = models.ImageField(upload_to = 'person/', blank=True, null=True)
    position = models.CharField(max_length=150)
    organization = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    expertise = models.ManyToManyField(Topic, blank=True)
    department = models.ManyToManyField(Department, blank=True)
    is_active = models.BooleanField()
    description = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    highlight = models.BooleanField(default=False)
    order = models.PositiveIntegerField(blank=True,null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = ("People and Partner")
        verbose_name_plural = ("People and Partners")
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class TaggedProject(TaggedItemBase):
    content_object = models.ForeignKey('Project', on_delete=models.CASCADE)

class Project(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=160)
    department = models.ManyToManyField(Department, blank=True)
    project_member = models.ManyToManyField(Person)
    description = RichTextField()
    image = models.ImageField(upload_to = 'project/')
    periode_start = models.DateField(blank=True, null=True)
    periode_end = models.DateField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager(through=TaggedProject)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("Project")
        verbose_name_plural = ("Projects")
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

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
    category = models.ForeignKey(Publication_category, on_delete=models.CASCADE, blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL)
    topic = models.ManyToManyField(Topic, blank=True)
    department = models.ManyToManyField(Department, blank=True)
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