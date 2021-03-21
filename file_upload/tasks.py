# Create your tasks here

from celery import shared_task
from file_upload.models import Widget
from .models import Document
from .MQTT import MQTT_publisher
from .process import files_tmp_process,files_remove

import time
import subprocess
import os
import shutil

context ={} 
context["update"] = Document.objects.all()
other_files_path = 'D:/Edge-computing-platform/media/documents/'

@shared_task
def bsdiff_file(local_file,upload_file,file_name):

    local_file = local_file + ' '
    upload_file = upload_file + ' '
    file_patch = ' ' + file_name + '.patch'
    print(local_file)
    print(upload_file)

    if local_file != upload_file:
        print("working....")
        process_path = 'hdiffz' +' ' + '' + upload_file + '' + '' + local_file + '' + '' + file_patch + ''
        subprocess.call(process_path, shell=True, cwd= "D:\\Edge-computing-platform\\hdiff_hpatch\\")
        print('Processed')
        MQTT_publisher(context["update"])
        print('Sent Patch to client')
        print('Done!')
    else:
        print('1.0.0版本無須patch')
        zip_files,remove_files = files_tmp_process(context["update"])
        files_remove(remove_files)



