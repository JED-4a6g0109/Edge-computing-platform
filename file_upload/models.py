from django.db import models
from django.urls import reverse


from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class Document(models.Model):
    
    title = models.CharField(max_length=200,default='Model')
    description = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='Files')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    
    class Meta:
        db_table = 'file'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('file_edit', kwargs={'pk': self.pk})



@receiver(post_delete, sender=Document)
def submission_delete(sender, instance, **kwargs):
    removes = []
    if instance.document:
        model = instance.document.path.replace('zip', 'onnx')
        patch = instance.document.path.replace('zip', 'patch')
        upload_file = instance.document.path
        removes.append(model)
        removes.append(patch)
        removes.append(upload_file)
        for files in removes:
            if os.path.isfile(files):
                os.remove(files) 

        

class Widget(models.Model):
    name = models.CharField(max_length=140)