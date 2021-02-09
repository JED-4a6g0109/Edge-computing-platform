# Edge-computing-platform
## 研究概念
當大量的IOT設備要進行更新時，會導致伺服器癱瘓與篩車，或是需要用手動方式去更新模型。
為了方便設備選擇Model的版本與更新，實現了神經網路模型自動部屬平台，而此平台透過MQTT的方式通知IOT設備更新的訊息，
同時IOT設備會向Server進行Requset，Server接收後會傳送patch到IOT設備進行自動更新
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/MQTT.png)

- Django(Publisher)：只要上傳model就會發送更新訊息至Client。

- mosquitto(MQTT Broker)：中繼站負責Server與Client溝通橋樑。

- PySide Client(Subscribe)：接收Server發送過來的JSON並更新。


## 運用工具
 - Django開發Server平台
 - celery異步任務   >>[參考出處](https://github.com/celery/celery)
 - PySide模擬Client端
 - MQTT Mosquitto 扮演著Server與Client橋梁
 - MASK-RCNN遷移式學習   >>[參考出處](https://github.com/TannerGilbert/MaskRCNN-Object-Detection-and-Segmentation)
 - Keras與Tensorflow
 - bsdiff檔案二進制diff與patch   >>[參考出處](https://github.com/zhuyie/bsdiff)
 - labelme圖片的label   >>[參考出處](https://github.com/wkentaro/labelme)
 
## 主要套件控版與前置作業
此有詳細紀錄requirements.txt，可使用以下指令進行安裝
   
    pip install -r requirements.txt
    
### MQTT Mosquitto 安裝與設定

 - MQTT Mosquitto至官網[下載](https://mosquitto.org/download/)進行安裝
安裝完後開通開通防火牆埠號1883。Windows的防火牆預設沒有開通1883埠號，因此本機電腦以外的MQTT裝置無法和Mosquitto伺服器連線。

- 搜尋設定具有進階安全性的 windows defender 防火牆
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/MQTT1.jpg)</br>

- 規則類型設定
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/MQTT2.jpg)</br>

- 通訊協定設與連接埠設定
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/MQTT3.jpg)</br>

- 套用設定
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/MQTT4.jpg)</br>

- 名稱定義
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/MQTT5.jpg)</br>

- 開啟CMD輸入netstat -an|find “1883”測試是否有在運作，如果有正常則完成設定
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/MQTT6.jpg)</br>

### Django Server 路徑與IP設置部分

App>file_upload>process.py
<br>path變數部分須留意路徑設置，此參數的路徑為檔案上傳存放的資料夾/media/Files/</br>

    def folder_exists(dataset):
        """
        建立檔案名稱與檔案另名一致處理
        """
        files = []
        path = "D:/you_path/media/Files/"
        print(os.listdir(path))
        local_files = os.listdir(path)
        print("總共有",len(local_files),"檔案")
        new_path = ''
        dataset = dataset
        data_information(dataset)
        folder = path +  name
        if  not os.path.exists(folder):
            os.makedirs(folder)
        file_rename(folder)
        if rename_file in os.listdir(folder):
            print('已重新命名')
        for get_file in os.listdir(folder):
            files.append(get_file)
        upload_file_path = folder + '/' + str(files[-1])
        local_file_path = folder + '/' + str(files[0])
        file_name = folder + '/' + str(files[-1])[:-3]
        return upload_file_path,local_file_path,file_name
        
old_file_name需更改/media/" + file_name前的路徑
<br>new_file_name需更改/media/Files/" + rename_file</br>
       
    def file_rename(new_file_path):
        """
        檔案重新命名與更新object檔案路徑
        """
        global rename_file
        dot = file_name.find(".")
        extension = str(file_name[dot:])

        rename_file = name+"-"+version + extension

        old_file_name = "you_path/media/" + file_name
        new_file_name = "you_path/media/Files/" + rename_file

        os.rename(old_file_name,new_file_name)
        shutil.move(new_file_name,new_file_path)

        search_id = Document.objects.get(document=file_name)
        search_id.document = new_file_path + '/' + rename_file
        search_id.save()

App>file_upload>MQTT.py
<br>IP需更改</br>
<br>payload Download IP目前設置本機</br>

        IP = "you_IP"
        payload = {'Model_Name' : name , 'Description' : description,'Version' : version ,'Time' : t , 'Download' : "http://127.0.0.1:8000" + download_url}

App>file_upload>task.py
<br>subprocess.call的cwd路徑為bsdiff與bspatch存放路徑須注意</br>

        def bsdiff_file(local_file,upload_file,file_name):
            local_file = local_file + ' '
            upload_file = upload_file + ' '
            file_patch = ' ' + file_name + '.patch'

            if local_file != upload_file:
                print("working....")
                process_path = 'bsdiff' +' ' + '' + local_file + '' + '' + upload_file + '' + '' + file_patch + ''
                subprocess.call(process_path, shell=True, cwd= "D:\\Edge-computing-platform\\bsdiff4.2-win32\\")
                print('Processed')
            else:
                print('重複上傳相同檔案或單獨檔案無法patch')

### Django Server 與 celery 運行
上述設定無問題開始啟動Django Server與celery

    python manage.py runserver
    celery -A App worker -l info
    
Django Server

<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/django_run_server.jpg)</br>
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/index.jpg)</br>

celery
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/celery_run.jpg)</br>

   
   

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

