from distutils.command.upload import upload
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.utils.timezone import now
from embed_video.fields  import  EmbedVideoField
from datetime import date
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


# Create your models here.
class Department (models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(default='', editable=False, max_length=320)
    description = RichTextField(blank=True)
    image = models.ImageField(upload_to = 'media/dept', blank=True)
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
    photo = models.ImageField(upload_to = 'media/person', blank=True, null=True)
    position = models.CharField(max_length=150)
    organization = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    department = models.ManyToManyField(Department, blank=True)
    is_active = models.BooleanField()
    description = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = ("People")
        verbose_name_plural = ("Peoples")
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class TaggedProject(TaggedItemBase):
    content_object = models.ForeignKey('Project', on_delete=models.CASCADE)

class Project(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=160)
    department = models.ManyToManyField(Department, blank=True, null=True)
    project_member = models.ManyToManyField(Person)
    description = RichTextField()
    image = models.ImageField(upload_to = 'media/project')
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Person)
    category = models.ForeignKey(Publication_category, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department, blank=True)
    image = models.ImageField(upload_to = 'media/publication')
    file = models.FileField(upload_to='media/doc/')
    description = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    tags = TaggableManager(through=TaggedPublication)

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

class TaggedEvent(TaggedItemBase):
    content_object = models.ForeignKey('Event', on_delete=models.CASCADE)

class Event(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=320)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(default=now)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department, blank=True)
    image = models.ImageField(upload_to='media/event/img/')
    file = models.FileField(upload_to='media/event/file/', blank=True, null=True)
    link = models.URLField(blank=True)
    youtube = EmbedVideoField()
    description = RichTextField()
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
        return self.date_start.strftime('%d')

    def bln(self):
        return self.date_start.strftime('%B')

    @property
    def tglmulai(self):
        return self.date_end.strftime('%d %B %Y')
    
    @property
    def is_past_due(self):
        return date.today() > self.date


class TaggedNews(TaggedItemBase):
    content_object = models.ForeignKey('News', on_delete=models.CASCADE)

class News(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=160)
    date_release = models.DateField(default=now, blank=True, null=True)
    description = RichTextField()
    image = models.ImageField(upload_to = 'media/project')
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
