from pydub import AudioSegment
from pydub.playback import play
import socket
import sys
import threading

def send_request_to_server(request, host="localhost", port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.encode())
            response = s.recv(1024)
            return response
    except Exception as e:
        print(f"Error communicating with server: {e}")
        return None

def get_song():
    f = open(f"data/{title}/{title}_recv.mp3", "wb")
    for i in range(2662):
        response = send_request_to_server(f"{title}, {i}")
        f.write(response)

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: ")
    #     sys.exit(1)
    
    title = "song_2"
    # thread = threading.Thread(target=get_song)
    # thread.start()
    song = AudioSegment.from_mp3("data/song_2/song_2_recv.mp3")     
    play(song)

    
