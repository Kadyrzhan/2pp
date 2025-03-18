import pygame
import os

# Initialize pygame mixer and pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 300, 200
WHITE = pygame.Color(255, 255, 255)
MUSIC_FOLDER = "music"  # Ensure this folder exists with MP3 files
tracks = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
curr_track = 0
if tracks:
    pygame.mixer.music.load(tracks[curr_track])

def play_music():
    if tracks:
        pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_track():
    global curr_track
    if tracks:
        curr_track = (curr_track + 1) % len(tracks)
        pygame.mixer.music.load(tracks[curr_track])
        pygame.mixer.music.play()

def prev_track():
    global curr_track
    if tracks:
        curr_track = (curr_track - 1) % len(tracks)
        pygame.mixer.music.load(tracks[curr_track])
        pygame.mixer.music.play()

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill(WHITE)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_music()
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                prev_track()
    
    clock.tick(30)

pygame.quit()
