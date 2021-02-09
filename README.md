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



## 自定義function

### process.py/data_information()
需傳入QuerySet的參數型態
<br>也就是Document.objects.all()的QuerySet</br>
<br>再來將dataset傳入data_information()查詢最新上傳的dataset並回傳name,description,version,download_url這些資料</br>

    def data_information(dataset):
        """
        讀取資料詳細
        """
        global newest,download_url,file_name,name,description,version
        newest = len(dataset) -1
        download_url = str(dataset[newest].document.url)
        file_name = str(dataset[newest].document.name)
        name = str(dataset[newest])
        description = str(dataset[newest].description)       
        version = str(dataset[newest].version)

        return name,description,version,download_url
    
### process.py/folder_exists()
需傳入QuerySet的參數型態
<br>也就是Document.objects.all()的QuerySet</br>
<br>主要處理檔案群組分類與建立資料夾,並回傳三個變數</br>
<br>當檔案上傳時會先存入到..media/底下</br>
<br>而folder_exists()的工作就是把media的檔案搬移至File資料夾裡並進行group分類</br>
<br>group的分類目前是依照使用者上傳時Title所填的名稱來進行分類</br>
<br>這邊data_information()的部分不需重複宣告四個變數來存return值，因為在data_information()有設置global</br>

- upload_file_path model1.0.0的路徑
- local_file_path  model最新上傳時的路徑
- file_name        model的title名稱

變數解釋
- path             為總group分類的資料夾
- folder           為group分類的資料夾

      def folder_exists(dataset):
          """
          建立檔案名稱與檔案另名一致處理
          """
          files = []
          path = "D:/Edge-computing-platform/media/Files/"
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
         
### process.py/file_rename()
處理檔案命名與搬移至對應的group群組資料夾，並更新QuerySet的document路徑
變數解釋
- extension     副檔名
- rename_file   需重新命名的檔案
- old_file_name 檔案上傳時會在..media/底下的檔案的路徑
- new_file_name File資料夾裡的group路徑

      def file_rename(new_file_path):
         """
         檔案重新命名與更新object檔案路徑
         """
         global rename_file
         dot = file_name.find(".")
         extension = str(file_name[dot:])

         rename_file = name+"-"+version + extension

         old_file_name = "D:/Edge-computing-platform/media/" + file_name
         new_file_name = "D:/Edge-computing-platform/media/Files/" + rename_file

         os.rename(old_file_name,new_file_name)
         shutil.move(new_file_name,new_file_path)

         search_id = Document.objects.get(document=file_name)
         search_id.document = new_file_path + '/' + rename_file
         search_id.save()
            


### task.py/bsdiff_file()

為celery異部任務處理
<br>這邊負責bsdiff與bspatch在使用者上傳時會呼叫異部處理，以免Django Server卡在檔案上傳頁面無法動彈</br>
<br>local_file,upload_file,file_name三個參數為folder_exists()回傳的值</br>
<br>使用subprocess.call來執行外部的命令和程序</br>
<br>process_path主要設置bsdiff與bspatch的輸入格式</br>

    @shared_task
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

   

    
### MQTT.py/MQTT_publisher()
payloadJSON格式進行publish到subscribe客戶端傳遞最新檔案更新訊息
<br>MQTT_publisher也需傳入QuerySet的參數型態/br>
<br>再來將dataset傳入data_information()查詢最新上傳的dataset並回傳name,description,version,download_url這些資料</br>
    
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
            
 

### views.py/JSON_process()
QuerySet的資料型態用在html上有點不太好用，因此自己轉換成JSON格式並分組
<br>處理完後數據為左邊，經過JSON Editor工具可看到右邊資料被分層的很好處理的JSON格式</br>

<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/JSON.jpg)</br>

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


### views/filelist_view()
經過JSON_process()處理好資料格式後方便進行模板渲染 >>[參考出處](https://www.youtube.com/watch?v=1Pfien-Npdg&ab_channel=coderZworld)


    def filelist_view(request): 

        context ={} 
        context["dataset"] = Document.objects.all()
        context["group"] = Document.objects.values('title').distinct()

        data_serializers = serializers.serialize("json", Document.objects.all())
        JSON_data = JSON_process(data_serializers,context['group'])
        print(JSON_data)
        context["JSON_data"] = JSON_data 
        template = loader.get_template("model_list_view.html")
        res = template.render(context,request)
        return HttpResponse(res) 




            
### django-rest-framework
為了讓工程師在訓練完模型時，不必手上至Web Server而透過api方式post至Django上達到自動化
<br>開啟Django Server後輸入 http://127.0.0.1:8000/api/file_upload/可看到 Django REST framework頁面確認啟動成功  >>[參考出處](https://github.com/twtrubiks/django-rest-framework-tutorial)</br>

<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/web_api.jpg)</br>



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

## Mask RCNN 
train部分使用colab Mask RCNN對於內存容量非常要求，因此使用colab



#### MQTT subscribe(IOT Device、Client)
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


