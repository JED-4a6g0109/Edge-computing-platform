from django.shortcuts import render
from file_upload.froms import DocumentForm
from django.shortcuts import redirect
from .models import Document
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView,UpdateView
from django.shortcuts import (get_object_or_404, 
                              render, 
                              HttpResponseRedirect)        
from django.forms import ModelForm

from django.conf import settings                  
import json  
from .tasks import bsdiff_file
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework import viewsets

from file_upload.serializers import DocumentSerializer
from .process import folder_exists
from .MQTT import MQTT_publisher


class FileForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description','version', 'document']



def model_form_upload(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context ={} 
            context["dataset"] = Document.objects.all()

            local_file_path,upload_file_path,file_name = folder_exists(context["dataset"])

            bsdiff_file.delay(local_file_path,upload_file_path,file_name)
            
            context["update"] = Document.objects.all()

            MQTT_publisher(context["update"])

       
            return HttpResponseRedirect("/index/")
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {'form': form})


def filelist_view(request): 
    
    context ={} 
    context["dataset"] = Document.objects.all()
    context["group"] = Document.objects.values('title').distinct()

    data_serializers = serializers.serialize("json", Document.objects.all())
    JSON_data = JSON_process(data_serializers,context['group'])

    context["JSON_data"] = JSON_data 

    template = loader.get_template("modellist_view.html")
    res = template.render(context,request)
    return HttpResponse(res) 




def JSON_process(data,group_data):
    data = json.loads(data)
    process_data = []
    JSON_data = {}


    for count in range(len(data)):
        groups = ({'pk':data[count]['pk']})
        groups.update(data[count]['fields'])
        process_data.append(groups)

    for count in range(len(group_data)):
        JSON_data.setdefault(list(group_data[count].values())[0],[])

    for count in range(len(process_data)):
        for key in JSON_data.keys():
            if key == (process_data[count]['title']):
                JSON_data[key].append(process_data[count])
    return JSON_data




def file_update(request, pk, template_name='fileupdate.html'):
    file= get_object_or_404(Document, pk=pk)
    form = FileForm(request.POST or None, instance=file)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/index/")
    return render(request, template_name, {'form':form})



def file_delete(request, pk, template_name='file_confirm_delete.html'):
    file= get_object_or_404(Document, pk=pk)    
    if request.method=='POST':
        file.delete()
        return HttpResponseRedirect("/index/")
    return render(request, template_name, {'object':file})






# Create your views here.
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer




