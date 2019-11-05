import logging
import os
import re

from flask import current_app as app
from pyunpack import Archive

ALLOWED_EXTENSIONS = {'zip', 'rar', '7z'}
logging.getLogger().setLevel(logging.INFO)


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


def unzip_file_and_remove_zip_after(file_name, relative_current_path):
    logging.info('trying to extract {}'.format(file_name))
    _, extension = file_name.split('.')
    print(extension)
    try:
        extract_file(file_name, relative_current_path)
        delete_file(file_name)
    except Exception as e:
        delete_file(file_name)
        logging.error(e)
        raise Exception('Archivo corrupto o no soportado')


def extract_file(file_name, relative_current_path):
    Archive(os.path.join(app.config['UPLOAD_FOLDER'], file_name)).extractall(relative_current_path)


def delete_file(file_name):
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
                logging.info('*** removing file: {} from directory {}'.format(file, subdir))
                os.remove(os.path.join(subdir, file))
    logging.info('there have been removed {} files'.format(counter))
