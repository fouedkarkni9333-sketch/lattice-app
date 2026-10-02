import os
import zipfile
import zlib
from flask import Flask, render_template_string, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # السماح بملفات حتى 500 ميغابايت

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# الواجهة البسيطة والنظيفة (بدون نصوص معقدة، فقط رفع وتحميل)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منظومة الضغط السحابي</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: Tahoma, sans-serif; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #161b22; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: #58a6ff; }
        input[type="file"] { display: block; margin: 20px auto; padding: 15px; background: #21262d; color: #c9d1d9; border: 2px dashed #30363d; border-radius: 8px; width: 100%; cursor: pointer; }
        button { background-color: #238636; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background-color: #2ea043; }
        .download-btn { display: inline-block; margin-top: 25px; background-color: #1f6feb; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; }
        .download-btn:hover { background-color: #388bfd; }
    </style>
</head>
<body>
    <div class="container">
        <h2>منظومة الضغط السحابي للملفات</h2>
        <p>اختر الملفات أو الفيديوهات أو المجلدات لضغطها فوراً</p>
        
        <form method="POST" enctype="multipart/form-data" action="/compress">
            <input type="file" name="files" multiple required>
            <button type="submit">بدء الضغط والتنزيل</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>جاهز للتحميل</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: Tahoma, sans-serif; text-align: center; padding: 50px; }
        .container { max-width: 500px; margin: 0 auto; background: #161b22; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: #3fb950; }
        .download-btn { display: inline-block; margin-top: 20px; background-color: #238636; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold; }
        .download-btn:hover { background-color: #2ea043; }
        .back-link { display: block; margin-top: 20px; color: #8b949e; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>تم ضغط الملفات بنجاح!</h2>
        <p>حجم الملفات أصبح مصغراً وجاهزاً للحفظ في جهازك.</p>
        <a href="/download/{{ filename }}" class="download-btn">تحميل الملف المضغوط الآن</a>
        <a href="/" class="back-link">← العودة لرفع ملفات أخرى</a>
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
    
    # ضغط الملفات المرفوعة مباشرة في ملف أرشيف واحد
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            zipf.write(file_path, arcname=filename)
            os.remove(file_path) # تنظيف الملف المؤقت
            
    return render_template_string(RESULT_TEMPLATE, filename=archive_name)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
