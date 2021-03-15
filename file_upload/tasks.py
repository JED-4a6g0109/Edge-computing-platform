# Create your tasks here

from celery import shared_task
from file_upload.models import Widget
from .models import Document
from .MQTT import MQTT_publisher
from file_upload.compression import files_process,compression,files_remove

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
        process_path = 'bsdiff' +' ' + '' + local_file + '' + '' + upload_file + '' + '' + file_patch + ''
        subprocess.call(process_path, shell=True, cwd= "D:\\Edge-computing-platform\\bsdiff4.2-win32\\")
        print('Processed')
        MQTT_publisher(context["update"])
        print('done!')
    else:
        print('重複上傳相同檔案或單獨檔案無法patch')
        


