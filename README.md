# Edge-computing-platform
## 研究概念
當大量的IOT設備要進行更新時，會導致伺服器癱瘓與篩車，或是需要用手動方式去更新模型。
為了方便設備選擇Model的版本與更新，實現了神經網路模型自動部屬平台，而此平台透過MQTT的方式通知IOT設備更新的訊息，
同時IOT設備會向Server進行Requset，Server接收後會傳送patch到IOT設備進行自動更新
![image](https://github.com/JED-4a6g0109/Edge-computing-platform/blob/main/MQTT.png)

- Django(Publisher)：只要上傳model就會發送更新訊息至Client。

- mosquitto(MQTT Broker)：中繼站負責Server與Client溝通橋樑。

- PySide Client(Subscribe)：接收Server發送過來的JSON並更新。

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
 - 
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



## 自定義function

media_path = "D:/Edge-computing-platform/media/"

group_path = "D:/Edge-computing-platform/media/Files/"

tmp_path = "D:/Edge-computing-platform/media/documents/"

web_download_path = "http://127.0.0.1:8000/media/D%3A/Edge-computing-platform/media/Files/"

### process.py/data_information()
需傳入query dataset的參數型態
<br>也就是Document.objects.all()的query dataset</br>
<br>再來將dataset傳入data_information()查詢最新上傳的dataset並回傳name,description,version,download_url這些資料</br>

變數解釋
- newest      倒數最後一個為最新datase
- download_url上傳時預設的存放path
- file_name   上傳檔案存放path
- name        檔名
- description 表單description內容
- version     表單version內容
- dot         取得name.的位置
- extension   取得副檔名

      def data_information(dataset):
          global newest,download_url,file_name,name,description,version,dot,extension
          newest = len(dataset) -1
          download_url = str(dataset[newest].document.url)
          file_name = str(dataset[newest].document.name)
          name = str(dataset[newest])
          description = str(dataset[newest].description)       
          version = str(dataset[newest].version)
          dot = file_name.rfind(".")
          extension = str(file_name[dot:])

          return name,description,version,download_url
    
### process.py/folder_exists()
folder_exists(query dataset)

傳入為query dataset的參數型態

<br>也就是Document.objects.all()的query dataset</br>
<br>主要處理檔案群組分類與建立資料夾,並回傳三個變數</br>
<br>如果是zip檔會佔存至tmp_path裡</br>
<br>如果不是zip檔案上傳時會先存入到media_path底下</br>
<br>而folder_exists()的工作就是把media的檔案搬移至File資料夾裡並進行group分類</br>
<br>group的分類目前是依照使用者上傳時Title所填的名稱來進行分類</br>
<br>這邊data_information()的部分不需重複宣告四個變數來存return值，因為在data_information()有設置global</br>

- upload_file_path model最新上傳時的路徑
- local_file_path  model1.0.0的路徑
- file_name        group完重新命名後的路徑

變數解釋
- rename_file      重新命名path
- group_folde      為group分類的資料夾

      def folder_exists(dataset):
          files = []
          local_files = os.listdir(group_path)
          print("總共有",len(local_files),"群組")
          dataset = dataset
          data_information(dataset)
          group_folder = group_path +  name

          if  not os.path.exists(group_folder):
              os.makedirs(group_folder)

          rename_file = file_rename(group_folder)

          if rename_file in os.listdir(group_folder):
              print('已重新命名')

          for get_file in os.listdir(group_folder):
              dot = get_file.rfind(".")
              extension = str(get_file[dot:])
              if extension == '.h5':
                  files.append(get_file)

          files.sort()
          print(files)
          upload_file_path = group_folder + '/' + str(files[-1])
          local_file_path = group_folder + '/' + str(files[0])
          file_name = group_folder + '/' + str(files[-1])[:-3]

          return upload_file_path,local_file_path,file_name
         
### process.py/file_rename()
file_rename(group_folder)

傳入值為group的資料夾路徑

處理檔案命名與搬移至對應的group群組資料夾，並更新query dataset的document路徑

<br>變數解釋</br>
- extension     副檔名
- rename_file   需重新命名的名稱
- old_file_name 檔案上傳時會在media_path的檔案的路徑
- new_file_name group_path路徑
- tmp_file_path      佔存資料夾路徑
- search_id     query dataset查詢的id紀錄

      def file_rename(group_folder):
          rename_file = name+"-"+version + extension
          old_file_name = media_path + file_name
          new_file_name = group_path + rename_file
          tmp_file_path = tmp_path + rename_file

          if extension =='.zip':
              shutil.move(old_file_name,tmp_file_path)
              unzip(tmp_file_path,group_folder)   
          else:
              os.rename(old_file_name,new_file_name)
              shutil.move(new_file_name,group_folder)

          search_id = Document.objects.get(document=file_name)
          search_id.document = group_folder + '/' + rename_file
          search_id.save()

          return rename_file

### process.py/unzip()
unzip(path,path)

傳入值為佔存資料夾路徑與group的路徑,並依照group解壓縮至group_path正確位置

<br>變數解釋</br>
- rename_model     存重新命名的模型路徑
- files            壓縮檔裡所有資料名稱

      def unzip(tmp_file_path,model_path):
          model_path = model_path + '/'
          tmp_file_path = tmp_file_path
          rename_model = model_path + name+"-"+version + ".h5"
          zf = zipfile.ZipFile(tmp_file_path, 'r')
          files = zf.namelist()
          for file in files:
              dot = file.rfind(".")
              extension = str(file[dot:])
              if extension == '.h5':
                  zf.extract(file,model_path)
                  os.rename(model_path + file,rename_model)
              else:
                  zf.extract(file,tmp_path)

### process.py/compression()
compression(list)

return zip_files,remove_files type:list

傳入值為list,紀錄需要壓縮檔案的路徑，並回傳下載網址、名稱、敘述、版本

回傳值為下載路徑、名稱、敘述、版本

<br>變數解釋</br>
- files         存放所有需要壓縮檔案的路徑
- zip_name      壓縮名稱命名
- zip_path      壓縮檔案存放路徑
- New_FileName  對files檔案路徑裡取得檔名與副檔名 ex D:/test/model.h5 >> model.h5


      def compression(zip_files):
          files = zip_files
          zip_name = name + '-' + version + '.zip'
          zip_web_path = web_download_path + name + '/' + zip_name
          zip_path = group_path + name + '/' + zip_name

          with zipfile.ZipFile(zip_path, 'w') as zipF:
              for file in files:
                  New_FileName = file[file.rfind('/') +1 :]
                  zipF.write(file, compress_type=zipfile.ZIP_DEFLATED, arcname=New_FileName)#zipF如果不設定arcname的話會連同路徑壓縮進去會導致很多資料夾，所以要把路徑移除取得檔案名稱


          return zip_web_path,name,description,version


### process.py/files_tmp_process()
files_tmp_process(query dataset)

傳入值為query dataset，上傳zip檔案時會佔存至此壓縮檔會紀錄需要壓縮的檔案

以及把.h5模型搬移至Group做儲存並diff完後，統一壓縮labels、patch與您模型的設定檔


<br>變數解釋</br>
- zip_files         存放所有需要壓縮檔案的路徑
- remove_files      紀錄佔存需刪除的檔案
- upload_zip_path   存放zip上傳至佔存的路徑
- patch_name        patch檔案名稱
- path_patch        patch檔存放group的路徑

      def files_tmp_process(dataset):
          zip_files = []
          remove_files = []
          upload_zip_path = ""  
          dataset = dataset

          data_information(dataset)

          patch_name = name + '-' + version + '.patch'
          path_patch = group_path + name + "/" + patch_name

          zip_files.append(path_patch)

          if os.listdir(tmp_path) != []:
              for get_file in os.listdir(tmp_path):
                  dot = get_file.rfind(".")
                  extension = str(get_file[dot:])
                  if extension != '.zip':
                      zip_files.append(tmp_path + get_file)
                  else:
                      upload_zip_path = tmp_path + get_file
                  remove_files.append(tmp_path + get_file)

          print('要壓縮的檔案',zip_files)
          print('所有要刪除的檔案',remove_files)

          return zip_files,remove_files
    
    
### process.py/files_remove()
files_remove(list)

傳入值為一個list,刪除佔存資料夾檔案的路徑

      def files_remove(remove_files):
          files = remove_files
          for file in files:
              os.remove(file)
          print('files remove done!')

### task.py/bsdiff_file()
bsdiff_file(最新上傳時的路徑,model1.0.0的路徑,group完重新命名後的路徑)

為celery異部任務處理

<br>這邊負責bsdiff與bspatch在使用者上傳時會呼叫異部處理，以免Django Server卡在檔案上傳頁面無法動彈</br>
<br>local_file,upload_file,file_name三個參數為folder_exists()回傳的值</br>
<br>使用subprocess.call來執行外部的命令和程序</br>
<br>process_path主要設置bsdiff與bspatch的輸入格式</br>

    def bsdiff_file(local_file,upload_file,file_name):

        local_file = local_file + ' '
        upload_file = upload_file + ' '
        file_patch = ' ' + file_name + '.patch'
        print(local_file)
        print(upload_file)

        if local_file != upload_file:
            print("working....")
            process_path = 'hdiffz' +' ' + '' + upload_file + '' + '' + local_file + '' + '' + file_patch + ''
            subprocess.call(process_path, shell=True, cwd= diff_patch_path)
            print('Processed')
            MQTT_publisher(update_object_datas)
            print('Sent Patch to client')
            print('Done!')
        else:
            print('1.0.0版本無須patch')
            zip_files,remove_files = files_tmp_process(update_object_datas)
            files_remove(remove_files)

   

    
### MQTT.py/MQTT_publisher()
MQTT_publisher(query dataset)

payloadJSON格式進行publish到subscribe客戶端傳遞最新檔案更新訊息

<br>MQTT_publisher也需傳入QuerySet的參數型態/br>
<br>再來將dataset傳入data_information()查詢最新上傳的dataset並回傳name,description,version,download_url這些資料</br>
    
    
<br>變數解釋</br>
- t                 時間戳記
- download_zip      web下載路徑

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




