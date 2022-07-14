from django.db import models

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
