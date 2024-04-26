# Music Streaming

Required dependency:
- pyaudio
```
sudo apt install python3-pyaudio
```
<br/>

Run server using:
```
python3 server.py
```

Run client using:
```
python3 <song_title> <# of threads>
```

Expected file structure for storing music is:
- "data/<song_title>.wav"

<i>NOTE: Ensure hosts in both client.py and server.py match to successfully make connection</i>
