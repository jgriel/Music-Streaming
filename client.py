import pyaudio
import socket
import sys
import threading
from time import sleep

def send_request_to_server(request, host="172.233.74.25", port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((host, port))
            s.sendall(request.encode())
            response = s.recv(1024)
            return response
    except socket.timeout:
        print(f'Request {request} timed out')
        return None
    except Exception as e:
        print(f"Error communicating with server: {e}")
        return None


def stream_wav(thread_num, thread_count):
    dropped_packets = []
    i = thread_num

    while len(chunks) < size or len(dropped_packets) != 0:
        packet = i
        if len(dropped_packets) != 0:
            packet = dropped_packets[0]
            del dropped_packets[0]

        if packet >= size:
            break

        response = send_request_to_server(f'{title}, {packet}')

        if response == b'':
            dropped_packets.append(packet)
            print(f'packet {packet} dropped')
        else:
            chunks[packet] = response
            i += thread_count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: client.py <song_title> <threads>")
        sys.exit(1)
    
    title = sys.argv[1]
    
    response = send_request_to_server(f'{title}, PARAMS').decode('utf-8')
    if response[:5] == 'ERROR':
        print(response)
        sys.exit(1)

    params = response.split(', ')
    
    response = send_request_to_server(f'{title}, SPLIT')
    size = int.from_bytes(response, 'big')

    global chunks
    chunks = {}
    t = int(sys.argv[2])
    for i in range(t):
        thread = threading.Thread(target=stream_wav, args=[i, t])
        thread.start()

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(int(params[0])),
                    channels=int(params[1]),
                    rate=int(params[2]),
                    output=True)

    print(f'\n\n\n\n\n\n\n\n\n\nNow listening to: {title}')

    for i in range(size):
        while i not in chunks.keys():
            print('Buffering...')
            sleep(1)
            continue
        data = chunks[i]
        stream.write(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
