from file_upload.process import data_information
import os
import zipfile

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


def files_process(dataset):
    global name,description,version,file_name
    zip_files = []
    remove_files = []
    upload_zip_path = ""

    
    dataset = dataset
    name,description,version,file_name = data_information(dataset)
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