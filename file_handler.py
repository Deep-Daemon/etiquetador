from flask import Blueprint, render_template, abort, request, send_file, flash
from werkzeug.utils import secure_filename

from utils.file_utils import *

UPLOAD_FOLDER = './static/images'
ALLOWED_PATHS = ['temp', 'json']

file_handler = Blueprint('files', __name__,
                         template_folder='templates/files')


@file_handler.route('/file', methods=['GET'])
def file_index():
    return render_template('file.html')


@file_handler.route('/upload_file', methods=['POST'])
@file_handler.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        verify_exists_file_in_request(request)
        file = request.files['file']
        verify_not_empty_name_file(file)
        if verify_not_empty_and_valid_file(file):
            file_name = secure_filename(file.filename)
            save_file(file_name, file)
            unzip_file_and_remove_zip_after(file_name, relative_current_path=app.config['UPLOAD_FOLDER'])
            remove_not_images_from_unzipped_folder(file_name)

            return "guardado exitosamente"
    except Exception as e:
        return str(e)


@file_handler.errorhandler(400)
def page_not_found(e):
    flash(str(e).split(':')[1])
    return render_template('400.html'), 400


@file_handler.route('/show_files/<path>', defaults={'page': 'index'})
@file_handler.route('/show_files/<path>')
def show_files(path):
    try:
        verify_accessible_path(path)
        list_files = os.listdir(os.path.join(app.static_folder, path))
        logging.info(list_files)
        if not list_files:
            raise Exception('No hay archivos en el directorio')

        return render_template("show_files.html", path=path, list_files=list_files)
    except Exception as e:
        logging.warning('Archivo no encontrado' + str(e))

        abort(400, description=str(e))


@file_handler.route('/download_file', methods=['POST'])
def download_file():
    if not request.form['file_name'] or not request.form['path']:
        return abort(400, description="No provided file name")
    try:
        return send_file(os.path.join(app.static_folder,
                                      request.form['path'], request.form['file_name']), as_attachment=True)
    except Exception as e:
        abort(404, description="Resource not found" + str(e))


def verify_accessible_path(path):
    if path not in ALLOWED_PATHS:
        raise Exception('path no permitido')
