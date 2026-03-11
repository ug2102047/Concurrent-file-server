import socket
import threading
import time
import os
from app.units.logger import log_event

HOST = "127.0.0.1"
PORT = 5050
ACTIVE_CLIENTS = []

def handle_client(conn, addr):
    # Receive filename first, then spawn a dedicated transfer thread
    try:
        data = conn.recv(1024)
        if not data:
            conn.close()
            return
        filename = data.decode().strip()
        log_event(f"Client connected: {addr}") #os client er port number automticly generate korbe
        log_event(f"Requested file: {filename}")

        # Track active client
        ACTIVE_CLIENTS.append(addr)

        transfer_thread = threading.Thread(
            target=file_transfer_thread,
            args=(filename, conn, addr),
            daemon=True,
        )
        transfer_thread.start()

    except Exception as e:
        log_event(f"Error while handling client {addr}: {e}")
        try:
            conn.close()
        except Exception:
            pass

def start_file_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #you can use the ports of previous session
    server.bind((HOST, PORT))
    server.listen(5) #max 5 pendding request 

    log_event(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
        log_event(f"Active threads: {threading.active_count() - 1}")

def file_transfer_thread(filename, conn, addr):
    try:
        filepath = os.path.join(os.getcwd(), "files", filename)
        if not os.path.isfile(filepath):
            conn.sendall(b"ERROR: File not found")
            log_event(f"File not found: {filepath} for {addr}")
            return

        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(1000) 
                if not chunk:
                    break
                conn.sendall(chunk)
                
                time.sleep(0.2)

        log_event(f"File transfer completed for {addr} ({filename})")#After Successful Transfer

    except Exception as e:
        log_event(f"Error during transfer to {addr}: {e}")

    finally:
        try:
            conn.close() 
        except Exception:
            pass
        if addr in ACTIVE_CLIENTS:
            ACTIVE_CLIENTS.remove(addr)
        log_event(f"Client disconnected: {addr}") 
