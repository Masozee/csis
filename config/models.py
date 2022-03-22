from django.db import models
from django.forms import URLField

# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    link = URLField()
    image = models.ImageField(upload_to= 'media/slider')
    show = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ("Web Slider")
        verbose_name_plural = ("Web Slider")
