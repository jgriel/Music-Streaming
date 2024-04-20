from pydub import AudioSegment
from pydub.playback import play
from math import ceil
from os import path, mkdir

def split_song(song, song_name):
    num_frames = int(song.frame_rate * (len(song) / 1000))
    num_frames_packet = int((1024 * 8) / song.frame_width)
    num_packets = ceil(num_frames / num_frames_packet)

    for i in range(num_packets):
        start = num_frames_packet * i
        end = min(num_frames_packet * (i+1), num_frames)
        packet = song[start * 1000 // song.frame_rate : end * 1000 // song.frame_rate]

        if not path.exists(f"data/{song_name}/{song_name}_chunks"):
            mkdir(f"data/{song_name}/{song_name}_chunks")

        f = path.join(f"data/{song_name}/{song_name}_chunks/{song_name}_{i}.mp3")
        packet.export(f, format="mp3")

if __name__ == "__main__":
    song_name = "song_2"
    song = AudioSegment.from_mp3(f"data/{song_name}/{song_name}.mp3") 
    split_song(song, song_name)
    # print('playing sound using pydub')
    # play(song)
    

