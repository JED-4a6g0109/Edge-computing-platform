# Create your tasks here

from celery import shared_task
from file_upload.models import Widget

import time
import subprocess
import os
from .MQTT import MQTT_publisher_Patch

@shared_task
def bsdiff_file(local_file,upload_file,file_name):

    local_file = local_file + ' '
    upload_file = upload_file + ' '
    file_patch = ' ' + file_name + '.patch'

    process_path = 'bsdiff' +' ' + '' + local_file + '' + '' + upload_file + '' + '' + file_patch + ''
    subprocess.call(process_path, shell=True, cwd= "D:\\GnuWin32\\bsdiff4.2-win32\\")
    # MQTT_publisher_Patch()
    # print('Patch已傳置物聯網裝置')
    return("Processed!")



@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Widget.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()


@shared_task
def diff_filename(file1name,file2name):
    for line in difflib.unified_diff(file1name, file2name, fromfile='file1', tofile='file2', lineterm=''):
        print(line)