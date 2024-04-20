import socket
import threading
from os import path

def handle_client(conn, base_path):
    with conn:
        data = conn.recv(1024)
        request = data.decode().strip()
        print(f"{request}")
        args = request.split(', ')
        title = args[0]
        packet = args[1]

        file_path = f"data/{title}"

        if not path.exists(file_path):
            response = f"ERROR: {title} is not available"
            conn.sendall(response)
            return
        
        response = b''
        f = open(f"{file_path}/{title}_chunks/{title}_{packet}.mp3", "rb")
        for data in f:
            response += data

        conn.sendall(response)

def start_server(host='localhost', port=5000, base_path='.'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, base_path))
            thread.start()

if __name__ == "__main__":
    start_server(base_path='../music/')
