
import os
import shutil
from .models import Document
import zipfile
import json
from os import listdir
from os.path import isfile, isdir, join
import subprocess


#docker linux
media_path = "/Edge-computing-platform/media/"
group_path = "/Edge-computing-platform/media/Files/"
tmp_path = "/Edge-computing-platform/media/documents/"
web_download_path = "http://127.0.0.1:8888/media/Files/"

diff_patch_path = "/Edge-computing-platform/hdiff_hpatch/linux/"
name = ""
file_name = ""
description = ""
version = ""
extension = ""

def data_information(dataset):
    """
    data_information(query dataset)
    傳入值為query dataset
    取得最新一筆資料資訊
    """
    global file_name,name,description,version,extension
    newest = len(dataset) -1
    download_url = str(dataset[newest].document.url)
    file_name = str(dataset[newest].document.name)
    name = str(dataset[newest])
    description = str(dataset[newest].description)       
    version = str(dataset[newest].version)
    dot = file_name.rfind(".")
    extension = str(file_name[dot:])


        
def folder_exists(dataset):
    """
    folder_exists(query dataset)
    建立群組資料夾
    """

    dataset = dataset
    data_information(dataset)
    group_folder = group_path +  name + '/'

    if  not os.path.exists(group_folder):
        os.makedirs(group_folder)

    return group_folder



def file_rename(group_folder):
    """
    file_rename(path)
    將需要diff的檔案移至群組並重新命名加上version
    檔案重新命名與更新object檔案路徑
    """
    global name,file_name,extension

    upload_zip = name + '-' + version + '.zip'
    upload_zip_path = media_path + file_name
    tmp_file_path = tmp_path + upload_zip
    zip_path = group_path + name + '/' + upload_zip


    diff_files = []
    patch_files = []
    upload_files = []


    if extension =='.zip':
        shutil.move(upload_zip_path,tmp_file_path)
        files = unzip(tmp_file_path)


        if "config.json" in files:

            with open(tmp_path+ 'config.json') as f:
                config = json.load(f)

            for get_file in config["diff"]:
                dot = get_file.rfind(".")
                extension = str(get_file[dot:])


                old_name = tmp_path + get_file
                rename =  get_file[:dot] + "-" + version + extension
                rename_path = tmp_path + rename


                diff_first_path = group_folder + get_file[:dot] + "-" + "1.0.0" + extension
                diff_files.append(diff_first_path)

                upload_path = group_folder + get_file[:dot] + "-" + version + extension
                upload_files.append(upload_path)

                patch_file_path = group_folder + get_file[:dot] + "-" + version + ".patch"
                patch_files.append(patch_file_path)

                shutil.move(old_name,group_folder + rename)


            search_id = Document.objects.get(document=file_name)
            search_id.document = group_folder + upload_zip
            search_id.save()

            


            return diff_files,upload_files,patch_files,zip_path,tmp_file_path
        
        else:
            print('not config.json,pleas check!')


    else:
        print('not .zip file')



    

def unzip(tmp_file_path):
    """
    unzip(path)
    傳入值為壓縮檔路徑
    進行解壓縮與回傳.zip裡所有檔案名稱
    """
    print(tmp_file_path)
    zf = zipfile.ZipFile(tmp_file_path, 'r')
    zf.extractall(tmp_path)
    files = zf.namelist()

    zf.close()

    return files



def compression(zip_files,zip_path):
    """
    compression(list,path)
    傳入值為需壓縮的所有檔案與建立壓縮檔

    回傳名稱、敘述、建立壓縮檔下載點、版本

    """
    global name,description,version

    context ={} 
    context["dataset"] = Document.objects.all()
    data_information(context["dataset"])
    files = zip_files
    files.append(tmp_path + 'config.json')
    zip_name = name + '-' + version + '.zip'
    zip_web_path = web_download_path + name + '/' + zip_name
    print('zip path',zip_web_path)
    with zipfile.ZipFile(zip_path, 'w') as zipF:
        for file in files:
            New_FileName = file[file.rfind('/') +1 :]
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED, arcname=New_FileName)


    return zip_web_path,name,description,version



def tmp_files_remove():
    """
    刪除佔存資料夾所有檔案
    """

    files = listdir(tmp_path)
    for f in files:
        fullpath = join(tmp_path, f)
        if isfile(fullpath):
            os.remove(tmp_path + f)

    print('files remove done!')


def diff(diif_first,diff_second,patch,count):
    """
    diff(diff_file1,diff_file2,patch,count)
    傳入值為diff兩個檔案路徑與patch儲存路徑，count為記錄處理次數
    """

    print("working" + str(count+1) + "diff")
    process_path = './hdiffz' +' ' + '' + diif_first + ' ' + diff_second + ' ' + patch + ''
    print(process_path)
    subprocess.call(process_path, shell=True, cwd= diff_patch_path)
    print('Processed')



def cmp(a, b):
    """
    cmp(any_type,any_type)
    傳入值任何型態，並兩者比較是否相同
    """
    return (a > b) - (a < b) 