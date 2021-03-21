import paho.mqtt.client as mqtt
import datetime 
import json
from .models import Document


from .process import files_tmp_process,compression,files_remove


IP = "192.168.137.1"
PORT = 1883


def MQTT_publisher(dataset):
    dataset = dataset


    try:
        zip_files,remove_files = files_tmp_process(dataset)
        download_zip,name,description,version = compression(zip_files)
        files_remove(remove_files)


        client = mqtt.Client()
        client.connect(IP, PORT, 60)
        
        ISOTIMEFORMAT = '%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        payload = {'Model_Name' : name , 'Description' : description,'Version' : version ,'Time' : t , 'Download' : download_zip}

        print (json.dumps(payload))
        client.publish("pushnotification", json.dumps(payload))
                
    except Exception as e:
        print(e)




    
