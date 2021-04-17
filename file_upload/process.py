
import os
import shutil
from .models import Document
import zipfile

#Win10
# media_path = "D:/Edge-computing-platform/media/"
# group_path = "D:/Edge-computing-platform/media/Files/"
# tmp_path = "D:/Edge-computing-platform/media/documents/"
# web_download_path = "http://127.0.0.1:8000/media/D%3A/Edge-computing-platform/media/Files/"


#docker linux
media_path = "/Edge-computing-platform/media/"
group_path = "/Edge-computing-platform/media/Files/"
tmp_path = "/Edge-computing-platform/media/documents/"
web_download_path = "http://127.0.0.1:8888/media/Files/"

def data_information(dataset):
    """
    取得query dataset最新資料
    """
    global newest,download_url,file_name,name,description,version,dot,extension
    newest = len(dataset) -1
    download_url = str(dataset[newest].document.url)
    file_name = str(dataset[newest].document.name)
    name = str(dataset[newest])
    description = str(dataset[newest].description)       
    version = str(dataset[newest].version)
    print(version)
    dot = file_name.rfind(".")
    extension = str(file_name[dot:])

    return name,description,version,download_url

        
def folder_exists(dataset):
    """
    建立檔案名稱與檔案另名一致處理
    """
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
    

def file_rename(group_folder):
    """
    檔案重新命名與更新object檔案路徑
    """
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
    

def unzip(tmp_file_path,model_path):
    """
    unzip(path,path)
    傳入值為佔存資料夾路徑與group的路徑
    並依照group解壓縮至group_path正確位置
    """
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

    




def compression(zip_files):
    """
    compression(list)
    return zip_files,remove_files type:list
    傳入值為list,紀錄需要壓縮檔案的路徑，並回傳下載網址、名稱、敘述、版本
    """
    files = zip_files
    zip_name = name + '-' + version + '.zip'
    zip_web_path = web_download_path + name + '/' + zip_name
    zip_path = group_path + name + '/' + zip_name

    with zipfile.ZipFile(zip_path, 'w') as zipF:
        for file in files:
            New_FileName = file[file.rfind('/') +1 :]
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED, arcname=New_FileName)


    return zip_web_path,name,description,version


def files_tmp_process(dataset):
    global version
    """
    files_tmp_process(query dataset)
    傳入值為query dataset，上傳zip檔案時會佔存至此壓縮檔會紀錄需要壓縮的檔案，
    以及把.h5模型搬移至Group做儲存並diff完後，統一壓縮labels、patch與您模型的設定檔
    """

    zip_files = []
    remove_files = []
    upload_zip_path = ""  
    dataset = dataset

    data_information(dataset)
    print(version)

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
    

def files_remove(remove_files):
    """
    files_remove(list)
    傳入值為一個list,刪除佔存資料夾檔案的路徑
    """
    files = remove_files
    for file in files:
        os.remove(file)
    print('files remove done!')