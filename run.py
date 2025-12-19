from app.server.file_server import start_file_server
from app.web.routes import start_web
import threading


def main():
	server_thread = threading.Thread(target=start_file_server, daemon=True)
	server_thread.start()

	start_web()

if __name__ == "__main__":
	main()