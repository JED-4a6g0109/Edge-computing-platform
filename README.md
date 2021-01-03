# Edge-computing-platform
Edge-computing-platform

## MQTT subscribe(IOT Device、Client)
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish 
    import time
    import requests
    import shutil

    IP = "192.168.50.199"
    PORT = 1883
    URL = ""

    def download_file(url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            with open('D:\\Download\\' + local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        return local_filename

    def on_connect(client, userdata, flags, rc):
        print("已連線 "+str(rc))
        client.subscribe("pushnotification")

    def on_message(client, userdata, msg):
        print(msg.topic+" "+ msg.payload.decode('utf-8'))
        pushnotification_message = eval(msg.payload.decode('utf-8'))
        URL = pushnotification_message['Download']
        download_file(URL)
        print('Download Model complete')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(IP, PORT, 60)
    client.loop_start()

## Model training automation
    import requests
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    multipart_data = MultipartEncoder(
        fields={
        'title': 'vg',
        'description': 'hello',
        'version': '1.0.3',
        'document': ('vg.h5',open('C:\\Users\\tomto\\py\\vg.h5', 'rb'), 'text/plain')
    }
        )
    response = requests.post('http://127.0.0.1:8000/api/file_upload/', data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})
    print(response)

