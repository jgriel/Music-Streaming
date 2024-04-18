import socket
import sys

def send_request_to_server(request, host="localhost", port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.encode())
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        print(f"Error communicating with server: {e}")
        return None

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: ")
    #     sys.exit(1)
    
    for i in range(1,5):
        print(send_request_to_server(str(i)))
