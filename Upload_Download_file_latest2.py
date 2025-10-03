from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string
import os
import mimetypes

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_file_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type == 'application/pdf':
            return 'pdf'
        elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'word'
        elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return 'excel'
        elif mime_type in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
            return 'powerpoint'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type.startswith('text/'):
            return 'text'
    return 'other'

HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>📂 File Transfer Hub</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
      min-height: 100vh;
      padding: 40px 20px;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #e0e0e0;
    }
    
    .container {
      max-width: 800px;
      margin: auto;
    }
    
    .header {
      text-align: center;
      margin-bottom: 40px;
      animation: fadeInDown 0.8s ease;
    }
    
    .header h1 {
      font-size: 2.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 10px;
    }
    
    .header p {
      color: #a0a0a0;
      font-size: 1.1rem;
    }
    
    .glass-card {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 30px;
      margin-bottom: 30px;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
      animation: fadeInUp 0.8s ease;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
    }
    
    .card-title {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: #ffffff;
    }
    
    .card-title i {
      color: #667eea;
    }
    
    .upload-form {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    
    .form-control {
      background: rgba(255, 255, 255, 0.08);
      border: 2px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      color: #ffffff;
      padding: 12px 16px;
      transition: all 0.3s ease;
      flex: 1;
      min-width: 200px;
    }
    
    .form-control:focus {
      background: rgba(255, 255, 255, 0.12);
      border-color: #667eea;
      box-shadow: 0 0 0 0.25rem rgba(102, 126, 234, 0.25);
      color: #ffffff;
      outline: none;
    }
    
    .form-control::file-selector-button {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      color: white;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      margin-right: 12px;
    }
    
    .form-control::file-selector-button:hover {
      transform: scale(1.05);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .btn-upload {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      color: white;
      padding: 12px 32px;
      border-radius: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    
    .btn-upload:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    .file-list {
      list-style: none;
      padding: 0;
      margin-top: 20px;
    }
    
    .file-item {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 12px;
      transition: all 0.3s ease;
      animation: slideIn 0.5s ease;
    }
    
    .file-item:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(102, 126, 234, 0.5);
    }
    
    .file-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    
    .file-name {
      display: flex;
      align-items: center;
      gap: 12px;
      color: #ffffff;
      font-weight: 500;
      flex: 1;
      word-break: break-word;
    }
    
    .file-icon {
      color: #667eea;
      font-size: 1.2rem;
    }
    
    .file-actions {
      display: flex;
      gap: 8px;
    }
    
    .btn-preview, .btn-download {
      border: none;
      color: white;
      padding: 8px 16px;
      border-radius: 8px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.3s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      font-size: 0.9rem;
    }
    
    .btn-preview {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .btn-preview:hover {
      transform: scale(1.05);
      box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
    }
    
    .btn-download {
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .btn-download:hover {
      transform: scale(1.05);
      box-shadow: 0 4px 12px rgba(56, 239, 125, 0.4);
      color: white;
    }
    
    .preview-container {
      margin-top: 15px;
      padding: 15px;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 10px;
      display: none;
      max-height: 500px;
      overflow: auto;
    }
    
    .preview-container.active {
      display: block;
      animation: slideDown 0.3s ease;
    }
    
    .preview-container img {
      max-width: 100%;
      border-radius: 8px;
      display: block;
      margin: 0 auto;
    }
    
    .preview-container iframe {
      width: 100%;
      min-height: 500px;
      border: none;
      border-radius: 8px;
      background: white;
    }
    
    .preview-text {
      color: #e0e0e0;
      font-family: 'Courier New', monospace;
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    
    .empty-state {
      text-align: center;
      padding: 40px 20px;
      color: #a0a0a0;
    }
    
    .empty-state i {
      font-size: 4rem;
      color: #667eea;
      margin-bottom: 20px;
      opacity: 0.5;
    }
    
    @keyframes fadeInDown {
      from {
        opacity: 0;
        transform: translateY(-30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateX(-20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }
    
    @keyframes slideDown {
      from {
        opacity: 0;
        max-height: 0;
      }
      to {
        opacity: 1;
        max-height: 500px;
      }
    }
    
    @media (max-width: 768px) {
      .upload-form {
        flex-direction: column;
      }
      
      .file-header {
        flex-direction: column;
        gap: 12px;
        align-items: flex-start;
      }
      
      .file-actions {
        width: 100%;
      }
      
      .btn-preview, .btn-download {
        flex: 1;
        justify-content: center;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1><i class="fas fa-cloud-upload-alt"></i> File Transfer Hub</h1>
      <p>Seamlessly share files across your network</p>
    </div>

    <div class="glass-card">
      <div class="card-title">
        <i class="fas fa-upload"></i>
        Upload Files
      </div>
      <form method="post" enctype="multipart/form-data" action="/upload" class="upload-form">
        <input class="form-control" type="file" name="file" required>
        <button class="btn-upload" type="submit">
          <i class="fas fa-paper-plane"></i>
          Upload
        </button>
      </form>
    </div>

    <div class="glass-card">
      <div class="card-title">
        <i class="fas fa-folder-open"></i>
        Your Files
        {% if file_data %}
          <span style="font-size: 0.9rem; color: #a0a0a0;">({{ file_data|length }})</span>
        {% endif %}
      </div>
      {% if file_data %}
        <ul class="file-list">
          {% for file in file_data %}
            <li class="file-item">
              <div class="file-header">
                <div class="file-name">
                  {% if file.type == 'image' %}
                    <i class="fas fa-image file-icon"></i>
                  {% elif file.type == 'pdf' %}
                    <i class="fas fa-file-pdf file-icon"></i>
                  {% elif file.type == 'word' %}
                    <i class="fas fa-file-word file-icon"></i>
                  {% elif file.type == 'excel' %}
                    <i class="fas fa-file-excel file-icon"></i>
                  {% elif file.type == 'video' %}
                    <i class="fas fa-file-video file-icon"></i>
                  {% elif file.type == 'audio' %}
                    <i class="fas fa-file-audio file-icon"></i>
                  {% elif file.type == 'text' %}
                    <i class="fas fa-file-alt file-icon"></i>
                  {% else %}
                    <i class="fas fa-file file-icon"></i>
                  {% endif %}
                  {{ file.name }}
                </div>
                <div class="file-actions">
                  {% if file.type in ['image', 'pdf', 'text'] %}
                    <button class="btn-preview" onclick="togglePreview('{{ file.name }}', '{{ file.type }}')">
                      <i class="fas fa-eye"></i>
                      Preview
                    </button>
                  {% endif %}
                  <a class="btn-download" href="{{ url_for('download_file', filename=file.name) }}">
                    <i class="fas fa-download"></i>
                    Download
                  </a>
                </div>
              </div>
              <div class="preview-container" id="preview-{{ loop.index0 }}">
                <!-- Preview content will be loaded here -->
              </div>
            </li>
          {% endfor %}
        </ul>
      {% else %}
        <div class="empty-state">
          <i class="fas fa-inbox"></i>
          <p>No files uploaded yet. Start by uploading your first file!</p>
        </div>
      {% endif %}
    </div>
  </div>

  <script>
    let activePreview = null;

    function togglePreview(filename, type) {
      const fileItems = document.querySelectorAll('.file-item');
      let targetIndex = -1;
      
      fileItems.forEach((item, index) => {
        const fileNameElement = item.querySelector('.file-name');
        if (fileNameElement.textContent.trim().includes(filename)) {
          targetIndex = index;
        }
      });

      if (targetIndex === -1) return;

      const previewContainer = document.getElementById(`preview-${targetIndex}`);
      
      if (activePreview === previewContainer && previewContainer.classList.contains('active')) {
        previewContainer.classList.remove('active');
        previewContainer.innerHTML = '';
        activePreview = null;
        return;
      }

      if (activePreview && activePreview !== previewContainer) {
        activePreview.classList.remove('active');
        activePreview.innerHTML = '';
      }

      if (!previewContainer.classList.contains('active')) {
        const encodedFilename = encodeURIComponent(filename);
        
        if (type === 'image') {
          previewContainer.innerHTML = `<img src="{{ url_for('view_file', filename='') }}${encodedFilename}" alt="${filename}">`;
        } else if (type === 'pdf') {
          previewContainer.innerHTML = `<iframe src="{{ url_for('view_file', filename='') }}${encodedFilename}"></iframe>`;
        } else if (type === 'text') {
          fetch(`{{ url_for('view_file', filename='') }}${encodedFilename}`)
            .then(response => response.text())
            .then(text => {
              previewContainer.innerHTML = `<div class="preview-text">${text}</div>`;
            })
            .catch(error => {
              previewContainer.innerHTML = `<p style="color: #ff6b6b;">Error loading preview</p>`;
            });
        }
        
        previewContainer.classList.add('active');
        activePreview = previewContainer;
      }
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    file_data = []
    for filename in files:
        file_data.append({
            'name': filename,
            'type': get_file_type(filename)
        })
    return render_template_string(HTML_PAGE, file_data=file_data)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(url_for("index"))
    file = request.files["file"]
    if file and file.filename.strip() != "":
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
    return redirect(url_for("index"))

@app.route("/files/<path:filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/view/<path:filename>")
def view_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)