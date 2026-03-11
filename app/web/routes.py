from flask import Flask, render_template, jsonify
from app.units.logger import LOG_DATA
from app.server.file_server import ACTIVE_CLIENTS
import os
import socket
from flask import Response, send_file, abort

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/logs")
def get_logs():
    return jsonify(LOG_DATA)

@app.route("/api/clients")
def get_clients():
    return jsonify(ACTIVE_CLIENTS)

@app.route("/api/files")
def get_files():
    files = []
    try:
        files = os.listdir(os.path.join(os.getcwd(), "files"))
    except Exception:
        files = []
    return jsonify(files)

def start_web():
    app.run(host="127.0.0.1", port=5000, debug=False) #debug=False → production mode

@app.route('/download/<path:filename>')
def download_file(filename):
    # sanitize filename to avoid path traversal
    safe_name = os.path.basename(filename)
    files_dir = os.path.join(os.getcwd(), 'files')
    filepath = os.path.join(files_dir, safe_name)
    if not os.path.isfile(filepath):
        return abort(404, description=f"File not found: {safe_name}")

    # stream data from the file-server TCP service to the HTTP client
    def stream_from_server():
        HOST = '127.0.0.1'
        PORT = 5050
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                # send the filename request
                s.sendall(safe_name.encode())

                # read until server closes
                while True:
                    chunk = s.recv(1024)
                    if not chunk:
                        break
                    # if server sends an error message as text, forward it and stop
                    if chunk.startswith(b'ERROR:'):
                        yield chunk
                        break
                    yield chunk
        except Exception as e:
            yield f"ERROR: {e}".encode()

    # return streaming response with attachment headers
    headers = {
        'Content-Disposition': f'attachment; filename="{safe_name}"'
    }
    return Response(stream_from_server(), mimetype='application/octet-stream', headers=headers)
