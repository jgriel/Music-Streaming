import pygame

if __name__ == "__main__":
    pygame.mixer.init()
    pygame.mixer.music.load("data/ye.mp3")
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue
