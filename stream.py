from pydub import AudioSegment
from pydub.playback import play

if __name__ == "__main__":
    song = AudioSegment.from_mp3("data/ye.mp3")
    print('playing sound using  pydub')
    play(song)
    

