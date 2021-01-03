
import os
import shutil
from .models import Document





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
    





