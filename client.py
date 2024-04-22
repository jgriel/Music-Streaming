import pyaudio
import socket
import sys
import threading

def send_request_to_server(request, host="localhost", port=5001):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.encode())
            response = s.recv(1024)
            return response
    except Exception as e:
        print(f"Error communicating with server: {e}")
        return None

def stream_wav():
    for i in range(size):
        response = send_request_to_server(f'{title}, {i}')
        chunks.append(response)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: client.py <song_title>")
        sys.exit(1)
    
    title = sys.argv[1]
    
    response = send_request_to_server(f'{title}, PARAMS').decode('utf-8')
    if response[:5] == 'ERROR':
        print(response)
        sys.exit(1)

    params = response.split(', ')
    
    response = send_request_to_server(f'{title}, SPLIT')
    size = int.from_bytes(response, 'big')

    chunks = []
    thread = threading.Thread(target=stream_wav)
    thread.start()

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(int(params[0])),
                    channels=int(params[1]),
                    rate=int(params[2]),
                    output=True)

    print(f'\n\n\n\n\n\n\n\n\n\nNow listening to: {title}')

    for i in range(size):
        data = chunks[i]
        stream.write(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
