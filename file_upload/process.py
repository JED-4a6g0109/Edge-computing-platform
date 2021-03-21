
import os
import shutil
from .models import Document
import zipfile


path = "D:/Edge-computing-platform/media/Files/"
path_labels = "D:/Edge-computing-platform/media/Labels/"


def data_information(dataset):
    """
    讀取資料詳細
    """
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

        
def folder_exists(dataset):
    """
    建立檔案名稱與檔案另名一致處理
    """
    global path
    files = []
    local_files = os.listdir(path)
    print("總共有",len(local_files),"群組")

    dataset = dataset
    data_information(dataset)
    folder = path +  name

    if  not os.path.exists(folder):
        os.makedirs(folder)
    

    rename_file = file_rename(folder)

    if rename_file in os.listdir(folder):
        print('已重新命名')

    for get_file in os.listdir(folder):
        dot = get_file.rfind(".")
        extension = str(get_file[dot:])
        if extension == '.h5':
            files.append(get_file)
    files.sort()
    print(files)
    upload_file_path = folder + '/' + str(files[-1])
    local_file_path = folder + '/' + str(files[0])
    file_name = folder + '/' + str(files[-1])[:-3]

    return upload_file_path,local_file_path,file_name
    

def file_rename(new_file_path):
    """
    檔案重新命名與更新object檔案路徑
    """
    rename_file = name+"-"+version + extension
    old_file_name = "D:/Edge-computing-platform/media/" + file_name
    new_file_name = "D:/Edge-computing-platform/media/Files/" + rename_file
    tmp_file_path = "D:/Edge-computing-platform/media/documents/" + rename_file
    if extension =='.zip':
        shutil.move(old_file_name,tmp_file_path)
        unzip(tmp_file_path,new_file_path)   
    else:
        os.rename(old_file_name,new_file_name)
        shutil.move(new_file_name,new_file_path)
        
    search_id = Document.objects.get(document=file_name)
    search_id.document = new_file_path + '/' + rename_file
    search_id.save()

    return rename_file
    

def unzip(tmp_file_path,model_path):
    tmp_path = "D:/Edge-computing-platform/media/documents/"
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

    



other_files_path = 'D:/Edge-computing-platform/media/documents/'

def compression(zip_files):
    files = zip_files
    zip_name = name + '-' + version + '.zip'
    zip_web_path = "http://127.0.0.1:8000/media/D%3A/Edge-computing-platform/media/Files/" + name + '/' + zip_name
    zip_path = "D:/Edge-computing-platform/media/Files/" + name + '/' + zip_name

    with zipfile.ZipFile(zip_path, 'w') as zipF:
        for file in files:
            New_FileName = file[file.rfind('/') +1 :]
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED, arcname=New_FileName)


    return zip_web_path,name,description,version


def files_tmp_process(dataset):
    # global name,description,version,file_name
    zip_files = []
    remove_files = []
    upload_zip_path = ""

    
    dataset = dataset
    data_information(dataset)
    patch_name = name + '-' + version + '.patch'
    path_patch = "D:/Edge-computing-platform/media/Files/" + name + "/" + patch_name
    zip_files.append(path_patch)

    if os.listdir(other_files_path) != []:
        for get_file in os.listdir(other_files_path):
            dot = get_file.rfind(".")
            extension = str(get_file[dot:])
            if extension != '.zip':
                zip_files.append(other_files_path + get_file)
            else:
                upload_zip_path = other_files_path + get_file
            remove_files.append(other_files_path + get_file)
    
    print('要壓縮的檔案',zip_files)
    print('所有要刪除的檔案',remove_files)
    
    return zip_files,remove_files
    

def files_remove(remove_files):
    files = remove_files
    for file in files:
        os.remove(file)
    print('files remove done!')