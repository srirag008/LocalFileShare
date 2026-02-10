import os
import socket
import threading
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Needed for showing "File Uploaded" messages

# Configure where files are saved
UPLOAD_FOLDER = 'uploads'
# This creates the folder if it doesn't exist yet
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_ip_address():
    """
    Finds your computer's IP address on the local network.
    This allows other devices (phones, laptops) to connect to you.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # We don't actually connect, but this tells the system to find the route
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1" # Fallback to localhost if offline
    finally:
        s.close()
    return ip_address

@app.route('/')
def index():
    """
    The Home Page.
    Lists all files currently in the 'uploads' folder.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # We pass the list of files and the IP address to the HTML page
    return render_template('index.html', files=files, ip=get_ip_address())

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads.
    """
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash(f'Successfully uploaded: {file.filename}')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """
    Allows users to download a file.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # host='0.0.0.0' makes the server accessible to other devices on the network
    # port=5000 is the standard Flask port
    print(f"Server running! Access it at http://{get_ip_address()}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)