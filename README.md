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




# ONNX-TensorRT-Jetson-nano

## Jetson nano使用前需準備的設備

- 支援Linux的無線網卡(本專案使用Alfa AWUS036NHA)(其他沒支援Linux網卡無法驅動...)

- 64GB以上的SD卡(本專案使用EVO Plus microSD 記憶卡 64GB)(強烈建議使用這張三星的其他張不是灌失敗就是奇怪問題一堆...)

- 滑鼠

- 鍵盤

- 螢幕(第一次安裝作業系統時需要用到後續用遠端就可以了)


## Jetson nano 安裝
強烈建議使用官方推薦的balenaEtcher來燒錄SD卡，如果懶得去官方下面有附檔案連結，因為每個Jetson nano映像檔都不同



[balenaEtcher](https://www.balena.io/etcher/)


[jetson nano developer kit 2gb 映像檔](https://drive.google.com/file/d/133wyVvOTEvIY4VWqVejrsVEbG9y7U_G2/view?usp=sharing)


燒錄過程中無腦一鍵完成，中間有問是否要格式都別裡

燒完後就是作業系統安裝如果開機第一次卡住超過10分鐘直接重開就行了

如果沒有近到ubuntu作業系統安裝代表SD卡燒錄失敗或是有問題或換SD卡

## Jetson nano 套件安裝

成功近到Ubuntu桌面後開始安裝遠端nomachine

不裝VNC是因為太慢了超級卡根本不能用，改用nomachine順暢非常多

[nomachine 載點](https://www.nomachine.com/download/download&id=115&s=ARM)

    
    wget https://www.nomachine.com/download/download&id=115&s=ARM
    sudo dpkg -i nomachine_your download version _arm64.deb

安裝好後去Ubuntu setting設定

改成開機不需密碼進入桌面，如果沒設定會一直停在登入畫面，而登入畫面網卡不會連線所以nomachine會連不進去

    User Accounts > UNLOCK > Automatic Login > ON

裝好後在你遠端電腦上安裝nomachine就可以用了，ip為 Jetson nano 網卡內網，密碼為Jetson nano登入密碼


## Jetson nano 環境變數設定

官網的映象擋都有內裝CUDA跟TensorRT所以只須設定下面的Ubuntu環境變數就可以了(建議使用官方的映象擋否則自裝CUDA會很多問題)

先安裝pip3

    sudo apt-get install python3-pip
 
設定環境變數

    sudo gedit  ~/.bashrc
    
到最下面新增，注意如果是TX2或其他板子請確定cuda的版本，一般Jetson nano是10.2，無果版本不對無法使用GPU

    #nvcc
    export CUBA_HOME=/usr/local/cuda-10.2
    export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH
    export PATH=/usr/local/cuda-10.2/bin:$PATH
    
    #python3.6
    export PYTHONPATH=/usr/lib/python3.6/dist-packages:$PYTHONPATH
    
## Jetson nano python套件安裝

原本是使用virtualenv不過問題一堆用到崩潰...

後來發現系統已經有python3.6了也安裝好tensorrt等套件跟設定，這邊就使用系統預安裝的python3.6

    pip3 install pycuda

安裝jupyter notebook

    pip3 install notebook
    
如果出現錯誤代表依賴套件沒裝好

    sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
    
開啟jupyter notebook

    ~/.local/bin/jupyter-notebook
    
onnx 安裝

    sudo apt-get install python-pip3 protobuf-compiler libprotoc-dev
    pip3 install Cython --user
    pip3 install onnx --user --verbose
    
    
ONNX Runtime安裝

    wget https://nvidia.box.com/shared/static/ukszbm1iklzymrt54mgxbzjfzunq7i9t.whl -O onnxruntime_gpu-1.7.0-cp36-cp36m-linux_aarch64.whl
    pip3 install onnxruntime_gpu-1.7.0-cp36-cp36m-linux_aarch64.whl
    
scikit-image安裝

    pip3 install scikit-image
    
出現 Pillow 安裝失敗請

    sudo apt-get install libjpeg-dev

出現 scipy 安裝失敗請

    sudo pip3 install scipy
    sudo apt-get install python-dev libfreetype6-dev
    sudo apt-get install libfreetype6-dev
    sudo ln -s /usr/include/freetype2/freetype/ /usr/include/freetype
    sudo apt-get install libfontconfig1-dev
    sudo pip3 install scikit-image

如果還有問題upgrade setuptools在安裝一次

    pip3 install --upgrade setuptools
    sudo pip3 install scikit-image
    
    
    
pytorch安裝(GPU版本)

參考文獻

https://forums.developer.nvidia.com/t/pytorch-and-cuda-on-jetson-xavier-nx/172928

https://forums.developer.nvidia.com/t/cannot-install-pytorch/149226
    
    pip3 install torchvision
    wget https://nvidia.box.com/shared/static/cs3xn3td6sfgtene6jdvsxlr366m2dhq.whl
    pip3 install torch-1.7.0-cp36-cp36m-linux_aarch64.whl
    
import torch有問題的話安裝

    sudo apt-get install libopenblas-base libopenmpi-dev 

如果有import 套件顯示Illegal instruction (core dumped)

是numpy問題

重新安装numpy==1.19.4
    
onnx tensorrt backend 安裝
    
    git clone --recursive https://github.com/onnx/onnx-tensorrt.git
    cd onnx-tensorrt
    mkdir build && cd build
 
 DGPU_ARCHS此參數為Jetson nano算力，如果是TX2或是其他板子要查詢，以免無法動
 
    cmake .. -DTENSORRT_ROOT=/usr/src/tensorrt -DGPU_ARCHS="53"
    make -j8
    sudo make install

 如果安裝沒失敗後回到onnx-tensorrt安裝python3 onnx_tensorrt backend

    cd onnx-tensorrt
    python3 setup.py build


如果遇到

CMake Error at CMakeLists.txt:3 (cmake_minimum_required):

CMake 3.13 or higher is required.  You are running version 3.10.2

(參考https://www.programmersought.com/article/39596499125/)

    把CMake砍掉重新安裝更高版本的
    sudo apt remove cmake
    sudo apt purge --auto-remove cmake
    version=3.13
    build=3
    mkdir ~/temp
    cd ~/temp
    wget https://cmake.org/files/v$version/cmake-$version.$build.tar.gz
    tar -xzvf cmake-$version.$build.tar.gz
    cd cmake-$version.$build/
    ./bootstrap
    make -j4
    sudo make install
    sudo cp ./bin/cmake /usr/bin/
    cmake --version
 
HDiffPatch安裝

https://github.com/sisong/HDiffPatch

    git clone https://github.com/sisong/HDiffPatch
    sudo apt-get install libboost-all-dev
    sudo apt-get install libbz2-dev
   
    make LZMA=0 ZSTD=0 MD5=0




到這安裝一帆風順的話恭喜可以使用 onnx、onnxruntime、onnx_tensorrt_backend、torch、gpu推論了....

    
## Pytroch flower 
使用Pytroch 訓練五朵花圖像辨識

在colab訓練前先下載資料集並上傳到雲端硬碟上，透過colab取得zip在解壓縮會比較快速，如果是上傳會非常慢

資料集來源：https://www.kaggle.com/alxmamaev/flowers-recognition

Colab 訓練https://colab.research.google.com/drive/1ILtnyGxCmnGh6aj2V0LHIfv9SqAPCd6z?usp=sharing

如果inference是使用自己電腦請參考[torch cuda安裝](https://varhowto.com/install-pytorch-cuda-10-2/)

需要留意每張顯卡支援的cuda版本都不一樣，本專案顯卡為1050、cu101、cuda10.1其他顯卡需要上網對映版本

訓練完後儲存model並轉換成onnx格式(注意這邊torch.load需要神經網路的類別>>[官方說明](https://pytorch.org/tutorials/beginner/saving_loading_models.html))
### 模型檔案
[onnx&pytroch_model](https://drive.google.com/drive/folders/1F_rH2kzwd-L6bPT4GqzFawKEdnE3GYyg?usp=sharing)


### model inference
    #模型辨識
    from PIL import Image
    import time

    model1 = torch.load('../content/models/entire_model80.pth')
    model1.eval()

    class_names = ['daisy', 'dandelion', 'rose', 'sunflower','tulip'] #class順序一定要跟訓練訓練一樣，否則映射錯誤

    image_PIL = Image.open('rose.jpg') 

    #圖片前處理
    transform = transforms.Compose([transforms.RandomHorizontalFlip(),
                                    transforms.RandomRotation(0.2),
                                    transforms.ToTensor(),
                                    transforms.Resize((80,80))
                                   ])

    image_tensor = transform(image_PIL)

    image_tensor.unsqueeze_(0)
    print(image_tensor.shape)

    image_tensor = image_tensor.to(device)
    print(image_tensor.shape)
    
    #主要 inference
    
    start = time.time()
    out = model1(image_tensor)
    end = time.time()

    print(out.shape)
    _, indices = torch.sort(out, descending=True)
    print(indices)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    print(percentage)
    prect = [(class_names[idx], percentage[idx].item()) for idx in indices[0][:1]]

    print('pred output:',prect[0][0])
    print('pred time:',end - start)


## torch convert to onnx

### ConvNet


    Accuracies = []
    class ConvNet(nn.Module):          # nn.Modules - base class for nn modules
        def __init__(self):
            super(ConvNet, self).__init__()


            # since colored images, so input channel = 3(For layer 1), then changes acoording to layers
            # stride - by how many pixel should our window moves
            # padding - how may 0's we want to add to our compressed image
            # Batch Normalization can improve lr of model, minimize internal covariate shift(mean-0, variance-1)
            # Max pooling will reduce th size of image into half



            # Layer 1
            self.layer1 = nn.Sequential(
                                            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=2),
                                            nn.BatchNorm2d(64),
                                            nn.ReLU(),
                                            nn.MaxPool2d(kernel_size=2, stride=2)
                                        )


            # Layer 2
            self.layer2 = nn.Sequential(
                                            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=2),
                                            nn.BatchNorm2d(128),
                                            nn.ReLU(),
                                            nn.MaxPool2d(kernel_size=2, stride=2)
                                        )


            # Layer 3
            self.layer3 = nn.Sequential(
                                            nn.Conv2d(128, 256, kernel_size=5, stride=1, padding=2),
                                            nn.BatchNorm2d(256),
                                            nn.ReLU(),
                                            nn.MaxPool2d(kernel_size=2, stride=2)
                                        )


            # Layer 4
            self.layer4 = nn.Sequential(
                                            nn.Conv2d(256, 512, kernel_size=5, stride=1, padding=2),
                                            nn.BatchNorm2d(512),
                                            nn.ReLU(),
                                            nn.MaxPool2d(kernel_size=2, stride=2)
                                        )


            # Layer 5
            self.layer5 = nn.Sequential(
                                            nn.Conv2d(512, 1024, kernel_size=5, stride=1, padding=2),
                                            nn.BatchNorm2d(1024),
                                            nn.ReLU(),
                                            nn.MaxPool2d(kernel_size=2, stride=2)
                                        )




            # fully connected network, applies linear transformation to the upcoming data
            # Fully Connected Layers
            self.fc1 = nn.Linear(2*2*1024, 256)
            self.fc2 = nn.Linear(256, 512)
            self.fc3 = nn.Linear(512, 5)# put labels counts



        # Function to execute CNN
        def forward(self, x):
            out = self.layer1(x)
            out = self.layer2(out)
            out = self.layer3(out)
            out = self.layer4(out)
            out = self.layer5(out)
            out = out.reshape(out.size(0), -1)
            out = self.fc1(out)
            out = F.dropout(out, training=self.training)
            out = self.fc2(out)
            out = F.dropout(out, training=self.training)
            out = self.fc3(out)
            return F.log_softmax(out,dim=1)
    model = ConvNet().to(device)
    # Loss and optimizer

    criterion = nn.CrossEntropyLoss() # Used for classification problems
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001) # Default learning rate for Adam is 0.001


### convert to onnx
    # to onnx 
    import io
    import numpy as np
    from torch import nn
    import torch.utils.model_zoo as model_zoo
    import torch.onnx
    from torchvision import models    

    model = torch.load('flower3.pth')
    model.eval()
    print('Finished loading model!')
    print(model)
    device = torch.device("cuda")
    model = model.to(device)

    output_onnx = 'super_resolution.onnx'
    print("==> Exporting model to ONNX format at '{}'".format(output_onnx))
    input_names = ["input0"]
    output_names = ["output0"]
    inputs = torch.randn(1, 3, 80, 80).to(device)

    torch_out = torch.onnx._export(model, inputs, output_onnx, export_params=True, verbose=False,
                                   input_names=input_names, output_names=output_names)


## onnx use onnxruntime inference

    #onnxruntime 
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torchvision import datasets, transforms
    from torch.autograd import Variable
    import onnx
    from onnx_tf.backend import prepare
    import numpy as np
    from IPython.display import display
    from PIL import Image
    import time

    import onnxruntime as rt
    import numpy
    from skimage.transform import resize
    from skimage import io
    import time

    img = io.imread("123.jpg")
    img = np.rollaxis(img, 2, 0) 
    img224 = resize(img / 255, (3, 80, 80), anti_aliasing=True)
    ximg = img224[np.newaxis, :, :, :]
    ximg = ximg.astype(np.float32)
    print(ximg.shape)

    class_names = ['daisy', 'dandelion', 'rose', 'sunflower','tulip']

    sess = rt.InferenceSession("super_resolution.onnx")

    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name

    try:
        start = time.time()
        y = sess.run(None, {input_name: ximg})
        end = time.time()
        print(class_names[np.argmax(y)])
        print('pred time:',end - start)
    except Exception as e:
        print("Misspelled output name")
        print("{0}: {1}".format(type(e), e))

## python backend tensorrt inference

確認是否有使用GPU

    import torch

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

載入onnx模型

    #load model
    import onnx
    import onnx_tensorrt.backend as backend
    import numpy as np
    from skimage.transform import resize
    from skimage import io
    import time
    model = onnx.load("flower3.onnx")
    engine = backend.prepare(model, device='CUDA:0')

開始推理

    #pred
    img = io.imread("dandelion1.jpg")
    img = np.rollaxis(img, 2, 0) 
    resize_img = resize(img / 255, (3, 80, 80), anti_aliasing=True)
    resize_img = resize_img[np.newaxis, :, :, :]
    flat32_img = resize_img.astype(np.float32)

    class_names = ['daisy', 'dandelion','tulip']


    start = time.time()

    output_data = engine.run(flat32_img)[0]

    end = time.time()
    print(output_data)
    print(output_data.shape)

    print(class_names[np.argmax(output_data)])
    print('pred time:',end - start)


## Auto patch & restart script

    #!/usr/bin/env python
    # coding: utf-8

    # In[18]:


    #client訂閱
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish 
    import time
    import requests
    import shutil
    import os
    import sys
    import zipfile
    import subprocess
    import subprocess

    folder = "/home/jed/Desktop/flower/"

    script_path = folder + "flower3_onnx_tensorrt.py"

    IP = "192.168.50.199"
    PORT = 1883
    URL = ""
    path = "flower.onnx"

    update_file = ""
    update_version = ""
    first_model = folder + "flower.onnx"
    first_labels = folder + "labels.txt"
    diff_patch_path = "/home/jed/HDiffPatch/"

    def download_file(url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_filename

    def on_connect(client, userdata, flags, rc):
        print("已連線 "+str(rc))
        client.subscribe("pushnotification")
        return "已連線 "+str(rc)

    def on_message(client, userdata, msg):
        global update_file,update_version,first_model,first_labels,path,folder

        print(msg.topic+" "+ msg.payload.decode('utf-8'))
        pushnotification_message = eval(msg.payload.decode('utf-8'))
        URL = pushnotification_message['Download']

        update_file = pushnotification_message['Model_Name']
        update_version = pushnotification_message['Version']

        zip_file = download_file(URL)
        print('Download Model complete')
        files = zip(zip_file)
        #     try:

        model_name = folder + "flower-" + update_version +".onnx"
        labels_name = folder + "labels1.txt"


        path = model_name
        for patch_file in files:

            if patch_file == "labels-1.0.1.patch":
                patch(first_labels,folder + patch_file,labels_name)
            else:
                patch(first_model,folder + patch_file,model_name)
        print("即將重啟")
        time.sleep(1)
        kill()
        time.sleep(1)
        restart()


    def zip(file):
        global path
        zf = zipfile.ZipFile(file, 'r')
        zf.extractall()
        files = zf.namelist()




        return files




    def patch(first_file,patch_file,output_file):

        process_path = './hpatchz' + ' ' + first_file + ' ' + patch_file  + ' ' + output_file + ''
        print(process_path)
        print('patching')
        subprocess.call(process_path, shell=True, cwd = diff_patch_path)
        print('Done!')




    def kill():
        global script_path
        command = 'pkill -f test.py' + script_path
        subprocess.call(command, shell=True)

    def restart():
        global script_path
        command = 'python3 ' + script_path
        subprocess.call(['xterm', '-e', command])

    def update_path(child_conn):
        global path
        child_conn.send(path)
        child_conn.close()



    if __name__ == '__main__':


            print("Script start !")
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(IP, PORT, 60)
            client.loop_start()




## Atuo script update tensorrt 


    #!/usr/bin/env python
    # coding: utf-8

    # In[ ]:


    from multiprocessing import Process,Queue,Pipe
    from update import update_path
    import torch
    #load model
    import onnx
    import onnx_tensorrt.backend as backend
    import numpy as np
    from skimage.transform import resize
    from skimage import io
    import time


    if __name__ == '__main__':
        #parent_conn,child_conn = Pipe()
        #p = Process(target=update_path, args=(child_conn,))
        #p.start()
        #model_path = parent_conn.recv()    
        model_path = "flower-1.0.1.onnx"

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print("load Neural network model")
        model = onnx.load(model_path)
        engine = backend.prepare(model, device='CUDA:0')
        print("load succeeded!")

        #pred

        print("prect sunflower.jpg")
        img = io.imread("sunflower.jpg")
        img = np.rollaxis(img, 2, 0) 
        resize_img = resize(img / 255, (3, 80, 80), anti_aliasing=True)
        resize_img = resize_img[np.newaxis, :, :, :]
        flat32_img = resize_img.astype(np.float32)

        class_names = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']


        start = time.time()
        print("tensorrt engine running...")
        output_data = engine.run(flat32_img)[0]

        end = time.time()
        print(output_data)
        print(output_data.shape)

        print(class_names[np.argmax(output_data)])
        print('pred time:',end - start)
