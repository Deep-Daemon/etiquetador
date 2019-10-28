import logging
import os
import re
import zipfile

from flask import current_app as app

ALLOWED_EXTENSIONS = {'zip', 'rar', '7z'}


def verify_exists_file_in_request(request):
    if 'file' not in request.files:
        raise Exception('No se pudo obtener el archivo')


def verify_not_empty_name_file(file):
    if file.filename == '':
        raise Exception('no seleccionaste ningún archivo')


def verify_not_empty_and_valid_file(file):
    if file and allowed_file(file.filename):
        return True
    else:
        raise Exception('Tu archivo no es válido')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(filename, file):
    relative_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(relative_file_name)


def unzip_file_and_remove_after_zip(file_name, relative_current_path):
    unzip(file_name, relative_current_path=relative_current_path)
    delete_zip(file_name)


def unzip(file_name, relative_current_path):
    relative_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    try:
        with zipfile.ZipFile(relative_file_name, 'r') as zip_ref:
            zip_ref.extractall(relative_current_path)
    except Exception as e:
        delete_zip(file_name)
        logging.error(e)
        raise Exception('No es un archivo zip')


def delete_zip(file_name):
    relative_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    os.remove(relative_file_name)


def remove_not_images_from_unzipped_folder(file_name):
    name_list_split = file_name.split('.')
    file_name = name_list_split[0]
    relative_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    counter = 0
    for subdir, dirs, files in os.walk(relative_file_name):
        for file in files:
            if not re.search('^([^.])+\\.(gif|jpg|jpeg|png|JPG|PNG|JPEG|GIF)$', file):
                counter += 1
                logging.info('*** removing file: {} from directory {}'.format(file_name, subdir))
                os.remove(os.path.join(subdir, file))
    logging.info('there have been removed {} files'.format(counter))
