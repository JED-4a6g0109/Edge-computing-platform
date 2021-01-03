from django.db import models
from django.urls import reverse

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

def name_getter(name, instance):
    return instance.label

class Document(models.Model):
    
    title = models.CharField(max_length=200,default='Model')
    description = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='Files')
    # document = models.FileField(upload_to='documents%Y-%m-%d-%H-%M-%S')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = 'file'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('file_edit', kwargs={'pk': self.pk})



class Widget(models.Model):
    name = models.CharField(max_length=140)