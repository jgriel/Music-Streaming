import socket
import sys

def send_request_to_server(request, host="localhost", port=53009):
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
    if len(sys.argv) < 2:
        print("Usage: python3 whimsi_client.py <route (e.g, localhost/hello.whimsi)>")
        sys.exit(1)
    
    route = sys.argv[1]
    host, file_path = route.split("/")

    hello_response = send_request_to_server("HELLO")
    print("SERVER SAYS:", hello_response)
