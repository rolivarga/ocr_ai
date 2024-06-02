from flask import Flask, request, jsonify, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def clear_session_uploads():
    if 'uploaded_files' in session:
        for filename in session['uploaded_files']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        session.pop('uploaded_files', None)

@app.before_request
def before_request():
    session.permanent = True
    if 'uploaded_files' not in session:
        session['uploaded_files'] = []

@app.after_request
def after_request(response):
    if not session:
        clear_session_uploads()
    return response

@app.route('/')
def index():
    files = session.get('uploaded_files', [])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        session['uploaded_files'].append(filename)
        return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200
    
    return jsonify({'message': 'File upload failed'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/generate', methods=['GET'])
def generate():
    text = main.generate_text()
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
