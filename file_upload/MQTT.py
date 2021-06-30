import paho.mqtt.client as mqtt
import datetime 
import json
from .models import Document
from .process import compression,tmp_files_remove

##

# docker linux
IP = "172.18.0.3"
PORT = 1883

def MQTT_publisher(zip_files,zip_path):
    """
    MQTT_publisher(zip_files,zip_path)
    zip_files type = list
    zip_path type = string
    傳入值為需要壓縮的files與zip路徑
    """

    try:

        download_zip,name,description,version = compression(zip_files,zip_path)
        tmp_files_remove()




        ISOTIMEFORMAT = '%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        payload = {'Model_Name' : name , 'Description' : description,'Version' : version ,'Time' : t , 'Download' : download_zip}
        message = json.dumps(payload)
        print (message)
        client = mqtt.Client()
        client.connect(IP, PORT, 60)
        client.publish("pushnotification", message)
       
                
    except Exception as e:
        print(e)




    
