import os
import zipfile
import zlib
from flask import Flask, render_template_string, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Allow files up to 500MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Lattice Compression</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: Tahoma, sans-serif; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #161b22; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: #58a6ff; }
        p { color: #8b949e; }
        input[type="file"] { display: block; margin: 20px auto; padding: 15px; background: #21262d; color: #c9d1d9; border: 2px dashed #30363d; border-radius: 8px; width: 100%; cursor: pointer; }
        button { background-color: #238636; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background-color: #2ea043; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Cloud Lattice Compressor</h2>
        <p>Select files, videos, or folders to compress instantly</p>
        
        <form method="POST" enctype="multipart/form-data" action="/compress">
            <input type="file" name="files" multiple required>
            <button type="submit">Start Compression & Download</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ready for Download</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: Tahoma, sans-serif; text-align: center; padding: 50px; }
        .container { max-width: 500px; margin: 0 auto; background: #161b22; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: #3fb950; }
        p { color: #8b949e; }
        .download-btn { display: inline-block; margin-top: 20px; background-color: #238636; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold; }
        .download-btn:hover { background-color: #2ea043; }
        .back-link { display: block; margin-top: 20px; color: #8b949e; text-decoration: none; }
        .back-link:hover { color: #58a6ff; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Files Compressed Successfully!</h2>
        <p>Your archive is ready and optimized for download.</p>
        <a href="/download/{{ filename }}" class="download-btn">Download Compressed ZIP</a>
        <a href="/" class="back-link">&larr; Back to Compressor</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/compress', methods=['POST'])
def compress_files():
    uploaded_files = request.files.getlist('files')
    if not uploaded_files or uploaded_files[0].filename == '':
        return redirect(url_for('index'))
    
    archive_name = "compressed_package.zip"
    archive_path = os.path.join(app.config['OUTPUT_FOLDER'], archive_name)
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            zipf.write(file_path, arcname=filename)
            os.remove(file_path)
            
    return render_template_string(RESULT_TEMPLATE, filename=archive_name)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
