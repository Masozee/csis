from operator import mod
from statistics import mode
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from taggit.managers import TaggableManager

# Create your models here.
class Department (models.Model):
    name = models.CharField(max_length=150)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ("Department")
        verbose_name_plural = ("Departments")

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
    photo = models.ImageField(upload_to = 'media/person')
    position = models.CharField(max_length=150)
    organization = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True)
    is_active = models.BooleanField()
    description = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = ("Person")
        verbose_name_plural = ("Persons")
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Publication_category(models.Model):
    name = models.CharField(max_length=150)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ("Publication Category")
        verbose_name_plural = ("Publication Category")


class Publication(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=320)
    authors = models.ManyToManyField(Person)
    category = models.ForeignKey(Publication_category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'media/publication')
    file = models.FileField(upload_to='media/doc/')
    description = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    tags = TaggableManager()

    def __str__(self):
        return self.name
        
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