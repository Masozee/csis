from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to= 'media/slider')
    show = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("Web Slider")
        verbose_name_plural = ("Web Slider")

class CodebookOrder(models.Model):
    cdid = models.PositiveIntegerField()
    ket = models.TextField()

    def __str__(self):
        return str(self.cdid)
        
    class Meta:
        verbose_name = ("Researcher Order")
        verbose_name_plural = ("Researcher Order")

class Career(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(default='', editable=False, max_length=320)
    content = RichTextField()
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Career tab")
        verbose_name_plural = ("Career tab")

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)