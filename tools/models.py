from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Shorten(models.Model):

    
    STATUS_CHOICES =(
        ('P', 'Publications'),
        ('E', 'Events'),
        ('A', 'Article'),
        ('M', 'Meeting'),
        ('O', 'Others'),
    )

    Judul = models.CharField(max_length=300,blank=True, null=True)
    ShortenWord = models.CharField(max_length=30, unique=True)
    Url = models.URLField()
    kategori = models.CharField(max_length=2, choices=STATUS_CHOICES)
    publish = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Judul
    
    class Meta:
        verbose_name = ("Shorten URL")
        verbose_name_plural = ("Shorten URL")

    @property
    def shorted(self):
        return f''

class selfhelp(models.Model):
    title = models.CharField(max_length=100)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("Support")
        verbose_name_plural = ("Support")

class Support_step(models.Model):
    support = models.ForeignKey(selfhelp, on_delete=models.CASCADE)
    step = models.CharField(max_length=300)
    proses = RichTextField()

    def __str__(self):
        return self.support

    class Meta:
        verbose_name = ("Support Step")
        verbose_name_plural = ("Support Step")