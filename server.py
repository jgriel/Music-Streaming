import socket
import threading

def handle_client(conn, addr, base_path):
    with conn:
        data = conn.recv(1024)
        request = data.decode().strip()
        print(f"{addr} - {request}")

        command = request.split(" ")[0]

        if command == "HELLO":
            response = "WORLD"
        conn.sendall(response.encode())

def start_server(host='localhost', port=53009, base_path='.'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, base_path))
            thread.start()

if __name__ == "__main__":
    start_server(base_path='../whimsi/')
