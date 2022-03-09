from flask import request, send_from_directory,Response
import os
import shutil
import io
import zipfile

from controllers import file_controller as controller

from utils import api_result 
import env
import json

@controller.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist('file')
    error = ""

    for file in uploaded_files:
        filename = file.filename
        file_ext = filename.split('.')[-1].lower()
        print(file_ext)
        if(file_ext not in ['bmp','png','jpg','jpeg']):
            error = 'illegal file type'
            break
        else:
            file.flush()
            shutil.rmtree(env.UPLOADED_IMG_FOLDER, ignore_errors=True)
            if not os.path.exists(env.UPLOADED_IMG_FOLDER):
                os.makedirs(env.UPLOADED_IMG_FOLDER)
            file.save(os.path.join(env.UPLOADED_IMG_FOLDER, filename))

    if error:
        return api_result.status_result(400, description=error)
    else:
        return api_result.status_result(200, "Success")

@controller.route('/<path:path>', methods=['GET'])
def get_img(path):
    return send_from_directory(env.UPLOADED_IMG_FOLDER,path)

def zip_folder():
    cwd = os.getcwd()

    os.chdir(env.DATA_FOLDER)

    buffer = io.BytesIO()
    zf = zipfile.ZipFile(buffer,'w',zipfile.ZIP_STORED)
    zf.write('label_data.json')
    zf.close()
    os.chdir(cwd)

    return buffer

@controller.route('/download_data', methods=['POST'])
def export_data():
    file_data = request.json
    
    try:
        os.remove(os.path.join(env.DATA_FOLDER, 'label_data.json'))
        os.remove(os.path.join(env.DATA_FOLDER, 'label_data.zip'))
    except OSError:
        pass
    with open(os.path.join(env.DATA_FOLDER,'label_data.json'),'w', encoding='utf-8') as f:
        json.dump(file_data, f, indent=4)
    # download files in the folder by fileIds
    memory_data = zip_folder()
    zip_file_name = 'label_data.zip'
    zip_path = os.path.join(env.DATA_FOLDER, zip_file_name)
     
    with open(zip_path, 'wb') as f:
        f.write(memory_data.getvalue())
        
    return send_from_directory(
        env.DATA_FOLDER,
        zip_file_name,
        as_attachment=True,
        attachment_filename=zip_file_name)

@controller.route('/download_data',methods=['GET'])
def download_data():
    if request.method == 'GET':
        filename = 'label_data.zip'
        # fullfilename = os.path.join(os.path.expanduser('~'), 'downloads', 'raw_data.zip')
        zip_path = os.path.join(env.DATA_FOLDER,filename)
        if os.path.exists(zip_path)==False:         
            return api_result(400,f"{zip_path} not found")
        #流式讀取
        def send_file():
            store_path = zip_path
            with open(store_path, 'rb') as targetfile:
                while 1:
                    data = targetfile.read(20 * 1024 * 1024)   # 每次讀取20M
                    if not data:
                        break
                    yield data

        response = Response(send_file(), content_type='application/octet-stream')
        response.headers["Content-disposition"] = 'attachment; filename=%s' % filename   # 如果不加上這行程式碼，導致下圖的問題
        # os.remove(fullfilename)
        return response