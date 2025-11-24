from flask import Blueprint, g, request, send_file

import os
import io
import zipfile
import tempfile
from multiprocessing import Pool
from PIL import Image
from extensions import csrf

tools_bp = Blueprint("tools", __name__, url_prefix="/tools")
csrf.exempt(tools_bp)


def convert_image(args):
    file_data, filename, output_format, temp_dir = args
    try:
        with Image.open(io.BytesIO(file_data)) as img:
            if img.mode != "RGB":
                img = img.convert('RGB')

            filename = safe_filename(filename)
            orig_ext = filename.rsplit('.', 1)[1] if '.' in filename else None

            ext = output_format.lower()
            if orig_ext:
                out_name = filename.replace(orig_ext, ext, 1)
            else:
                out_name = f"{filename}.{ext}"

            output_path = os.path.join(temp_dir, out_name)

            with open(output_path, 'wb') as f:
                img.save(f, format=output_format)

            return output_path, out_name, None
    except Exception as e:
        return None, filename, str(e)


def safe_filename(filename):
    filneame = filename.replace("/", "_").replace("..", "_")
    return filename


@tools_bp.before_app_request
def before_request():
    g.pool = Pool(processes=8)


@tools_bp.route('/', methods=['GET'])
@tools_bp.route('', methods=['GET'])
def tools_index():
    return send_file('index.html')


@tools_bp.route('/convert', methods=['POST'])
def convert_images():
    if 'files' not in request.files:
        return 'No files', 400

    files = request.files.getlist('files')
    output_format = request.form.get('format', '').upper()

    if not files or not output_format:
        return 'Invalid input', 400

    with tempfile.TemporaryDirectory() as temp_dir:
        file_data = []
        for file in files:
            if file.filename:
                file_data.append(
                    (file.read(), file.filename, output_format, temp_dir)
                )

        if not file_data:
            return 'No valid images', 400

        results = list(g.pool.map(convert_image, file_data))

        successful = []
        failed = []

        for path, name, error in results:
            if not error:
                successful.append((path, name))
            else:
                failed.append((name or 'unknown', error))

        if not successful:
            error_msg = "All conversions failed. " + \
                "; ".join([f"{f}: {e}" for f, e in failed])
            return error_msg, 500

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for path, name in successful:
                zf.write(path, name)

            if failed:
                summary = f"Conversion Summary:\nSuccessful: {len(successful)}\nFailed: {len(failed)}\n\nFailures:\n"
                summary += "\n".join([f"- {f}: {e}" for f, e in failed])
                zf.writestr("errors.txt", summary)

        zip_buffer.seek(0)

        return send_file(zip_buffer,
                         mimetype='application/zip',
                         as_attachment=True,
                         download_name=f'converted_{output_format.lower()}.zip')
