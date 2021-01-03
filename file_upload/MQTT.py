import paho.mqtt.client as mqtt
import datetime 
import json
from file_upload.process import data_information
from .models import Document


IP = "192.168.50.199"
PORT = 1883

def MQTT_publisher(dataset):
    dataset = dataset
    name,description,version,download_url = data_information(dataset)

    try:
        client = mqtt.Client()
        client.connect(IP, PORT, 60)
        ISOTIMEFORMAT = '%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        payload = {'Model_Name' : name , 'Description' : description,'Version' : version ,'Time' : t , 'Download' : "http://127.0.0.1:8000" + download_url}
        print (json.dumps(payload))
        client.publish("pushnotification", json.dumps(payload))
                
    except Exception as e:
        print(e)


def MQTT_publisher_Patch():
    context ={} 
    context["dataset"] = Document.objects.all()
    dataset = context["dataset"]
    name,description,version,download_url = data_information(dataset)

    dot_index = download_url.rindex('.')
    patch = download_url[:dot_index] + '.patch'
    try:
        client = mqtt.Client()
        client.connect(IP, PORT, 60)
        ISOTIMEFORMAT = '%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        payload = {'Model_Name' : name , 'Description' : description,'Version' : version ,'Time' : t , 'Download' : "http://127.0.0.1:8000" + patch}
        print (json.dumps(payload))
        client.publish("pushnotification", json.dumps(payload))
                
    except Exception as e:
        print(e)