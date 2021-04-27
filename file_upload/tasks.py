# Create your tasks here

from celery import shared_task
from file_upload.models import Widget
from .models import Document
from .MQTT import MQTT_publisher
from .process import tmp_files_remove,diff,cmp

import time
import os
import shutil



#docker linux
diff_patch_path = "/Edge-computing-platform/hdiff_hpatch/linux/"



@shared_task
def diff_mqtt_task(*variables):
    """
    diff_mqtt_task(diff_files,upload_files,patch_files,zip_path,tmp_file_path)
    diff_files type = list
    upload_files type = list
    patch_files type = list 
    zip_path type = string
    tmp_file_path type = string
    diff與mqtt任務，傳入值為需要diff、patch的資訊、建立zip路徑、暫存路徑
    """

    diff_files,upload_files,patch_files,zip_path,tmp_file_path = variables
    

    if cmp(diff_files,upload_files) != 0:
        print("working....")
        
        for index in range(len(diff_files)):
            diff(diff_files[index],upload_files[index],patch_files[index],index)

        MQTT_publisher(patch_files,zip_path)
        print('Sent Patch to client')
        print('Done!')

    else:
        print('1.0.0 version No need to patch')
        shutil.move(tmp_file_path,zip_path)
        tmp_files_remove()



