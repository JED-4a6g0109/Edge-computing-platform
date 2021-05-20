# Edge-computing-platform
## 研究概念
當大量的IOT設備要進行更新時，會導致伺服器癱瘓與篩車，或是需要用手動方式去更新模型。
為了方便設備選擇Model的版本與更新，實現了神經網路模型自動部屬平台，而此平台透過MQTT的方式通知IOT設備更新的訊息，
同時IOT設備會向Server進行Requset，Server接收後會傳送patch到IOT設備進行自動更新

![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/MQTT.png)

- Django(Publisher)：只要上傳model就會發送更新訊息至Client。

- mosquitto(MQTT Broker)：中繼站負責Server與Client溝通橋樑。

- PySide Client(Subscribe)：接收Server發送過來的JSON並更新。

## 詳細介紹
Youtube
https://www.youtube.com/watch?v=ISRpf_gjXcU&ab_channel=%E6%B4%AA%E5%B4%87%E6%81%A9

## 自動部屬影片實作
https://www.youtube.com/watch?v=13-eup1sNsA&feature=youtu.be&ab_channel=%E6%B4%AA%E5%B4%87%E6%81%A9

## 運用工具與出處
 - Django開發Server平台
 - celery異步任務   >>[參考出處](https://github.com/celery/celery)
 - PySide模擬Client端
 - MQTT Mosquitto 扮演著Server與Client橋梁
 - MASK-RCNN遷移式學習   >>[參考出處](https://github.com/TannerGilbert/MaskRCNN-Object-Detection-and-Segmentation)
 - Keras與Tensorflow
 - HDiffPatch檔案二進制diff與patch   >>[參考出處](https://github.com/sisong/HDiffPatch)
 - labelme圖片的label   >>[參考出處](https://github.com/wkentaro/labelme)
 
## 主要套件控版與前置作業
此有詳細紀錄requirements.txt，可使用以下指令進行安裝
   
    pip install -r requirements.txt

## Docker 

    git clone 此專案
    
    docker-compose run --service-ports django python3 manage.py runserver 0.0.0.0:8888
    
到這邊確認是否可開啟127.0.0.1:8888/index/

成功開啟後ctrl+c終止後下指令

    docker-compose up
    
docker-compose up完後會看到四個服務mosquitto、celery、django、redis

如果四個都有成功並正常運行代表OK沒意外mosquitto會開啟失敗顯示Error: Address not available

因為mosquitto2.0有變動需參考官方設定[Migrating from 1.x to 2.0](https://mosquitto.org/documentation/migrating-to-2-0/)

進入mosquitto的container後
  
    cd /mosquitto/config
    vi mosquitto.conf
    
更改設定
    
    listener 1883
    allow_anonymous true

改完後查mosquitto container log 就能看到mosquitto version 2.0.10 running

剩下就是把專案註解的docker linux給解開，環境就一鍵建置好了!

 - model_list_view.html
 - MQTT.py
 - process.py
 - task.py

docker-compose等設置參考[Very Academy](https://github.com/veryacademy/YT-Django-Docker-Compose-Celery-Redis-PostgreSQL)


## Docker System
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/Docker%20system.png)

## Use Case Diagram
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/use%20case%20diagram.png)

## Sequence Diagram
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/sequence%20diagram.png)



### Windown 10 MQTT Mosquitto 安裝與設定(使用docker可省略)

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

#### Windown10 
如果是使用Win10來執行請修改以下檔案，把docker linux換成 Win10的註解
 - model_list_view.html
 - MQTT.py
 - process.py
 - task.py






### Django Server 與 celery 運行
上述設定無問題開始啟動Django Server與celery

    python manage.py runserver
    celery -A App worker -l info
    
Django Server

<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/django_run_server.jpg)</br>
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/index.jpg)</br>

celery
<br>![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/celery_run.jpg)</br>


            
### django-rest-framework
為了讓工程師在訓練完模型時，不必手上至Web Server而透過api方式post至Django上達到自動化

這邊要注意如果是壓縮檔上傳只接受.zip檔名，rar、z7等壓縮格式不支援

<br>開啟Django Server後輸入 http://127.0.0.1:8000/api/file_upload/ 可看到 Django REST framework頁面確認啟動成功  >>[參考出處](https://github.com/twtrubiks/django-rest-framework-tutorial)</br>

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

#### 模擬train完後透過api上傳至Django Server後，Client自動下載與更新
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/api_upload.gif)



## Mask RCNN run Colab
[資料集](https://drive.google.com/file/d/1MdKIwDAuxOJIiLcwMXmuaYLMfDZrcgrK/view?usp=sharing)

train部分使用colab Mask RCNN對於內存容量非常要求，因此使用colab開啟進行traing
<br>如果是放置在colab請執行[Mask-Rcnn](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/Mask-Rcnn.ipynb)就沒問題了但須注意一些設定</br>

<br>FoodcontrollerConfig的需要注意NUM_CLASSES = 1+要訓練類別總數範例是9類</br>
- "Bitter_gourd"
- "Cabbage"
- "Potato"
- "Cucumber"
- "Cucumber_chips"
- "Garlic"
- "Chinese_cabbage"
- "Corn"
- "Onion"

      class FoodcontrollerConfig(Config):
          NAME = "Foodcontroller_segmentation"
          NUM_CLASSES = 1 + 9
          GPU_COUNT = 1
          IMAGES_PER_GPU = 1
          config = FoodcontrollerConfig()
          config.display()
          print(os.getcwd())

FoodDataset add class

    class FoodDataset(utils.Dataset):
        def load_dataset(self, dataset_dir):
            self.add_class('dataset', 1, 'Bitter_gourd')
            self.add_class('dataset', 2, 'Cabbage')
            self.add_class('dataset', 3, 'Potato')
            self.add_class('dataset', 4, 'Cucumber')
            self.add_class('dataset', 5, 'Cucumber_chips')
            self.add_class('dataset', 6, 'Garlic')
            self.add_class('dataset', 7, 'Chinese_cabbage')
            self.add_class('dataset', 8, 'Corn')
            self.add_class('dataset', 9, 'Onion')
            for i, filename in enumerate(os.listdir(dataset_dir)):
                if '.jpg' in filename:
                    self.add_image('dataset', 
                                   image_id=i, 
                                   path=os.path.join(dataset_dir, filename), 
                                   annotation=os.path.join(dataset_dir, filename.replace('.jpg', '.json')))

        def extract_masks(self, filename):
            json_file = os.path.join(filename)
            with open(json_file) as f:
                img_anns = json.load(f)

            masks = np.zeros([300, 400, len(img_anns['shapes'])], dtype='uint8')
            classes = []
            for i, anno in enumerate(img_anns['shapes']):
                mask = np.zeros([300, 400], dtype=np.uint8)
                cv2.fillPoly(mask, np.array([anno['points']], dtype=np.int32), 1)
                masks[:, :, i] = mask
                classes.append(self.class_names.index(anno['label']))
            return masks, classes

        def load_mask(self, image_id):
            info = self.image_info[image_id]
            path = info['annotation']
            masks, classes = self.extract_masks(path)
            return masks, np.asarray(classes, dtype='int32')

        def image_reference(self, image_id):
            info = self.image_info[image_id]
            return info['path']
        

## MQTT Client
使用pySide 有LGPL授權比較保險以下為Client自動更新檔案與介面，以下為Web上傳新版model自動更新與IOT Client介面和辨識
<br>[Client專案文檔與下載](https://github.com/JED-4a6g0109/Client)</br>
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/report_image/web_upload.gif)




