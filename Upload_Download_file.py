from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>📂 Local File Server</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { padding: 20px; background: #f8f9fa; }
    .container { max-width: 700px; margin: auto; }
    .card { margin-top: 20px; border-radius: 12px; }
    .btn-upload { background-color: #0d6efd; color: white; }
    .file-list li { margin: 6px 0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="text-center mb-4">
      <h1 class="display-5">📂 Local File Server</h1>
      <p class="text-muted">Upload and download files over your WiFi hotspot</p>
    </div>

    <div class="card p-4 shadow-sm">
      <h4>Upload a File</h4>
      <form method="post" enctype="multipart/form-data" action="/upload" class="d-flex gap-2 mt-2">
        <input class="form-control" type="file" name="file" required>
        <button class="btn btn-upload" type="submit">Upload</button>
      </form>
    </div>

    <div class="card p-4 shadow-sm">
      <h4>Uploaded Files</h4>
      {% if files %}
        <ul class="list-group file-list mt-3">
          {% for file in files %}
            <li class="list-group-item d-flex justify-content-between align-items-center">
              {{ file }}
              <a class="btn btn-sm btn-success" href="{{ url_for('download_file', filename=file) }}">Download</a>
            </li>
          {% endfor %}
        </ul>
      {% else %}
        <p class="text-muted mt-3">No files uploaded yet.</p>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_PAGE, files=files)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
