import pygame
import os
import sys

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen setup
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Music Player")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.SysFont('Arial', 24)

# Get all MP3 files in current directory
music_files = [f for f in os.listdir() if f.endswith('.mp3')]
if not music_files:
    print("No MP3 files found in current directory!")
    pygame.quit()
    sys.exit()

current_track = 0
paused = False

# Load first track
pygame.mixer.music.load(music_files[current_track])
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Control instructions
instructions = [
    "Space: Play/Pause",
    "S: Stop",
    "N: Next Track",
    "P: Previous Track",
    "+/-: Volume Up/Down",
    "Q: Quit"
]

def play_track():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.play()
        paused = False

def draw_interface():
    screen.fill(WHITE)
    
    # Current track info
    track_text = font.render(f"Now Playing: {music_files[current_track]}", True, BLACK)
    screen.blit(track_text, (20, 20))
    
    # Status
    status = "Paused" if paused else "Playing" if pygame.mixer.music.get_busy() else "Stopped"
    status_text = font.render(f"Status: {status}", True, BLACK)
    screen.blit(status_text, (20, 50))
    
    # Volume
    vol_text = font.render(f"Volume: {int(volume*100)}%", True, BLACK)
    screen.blit(vol_text, (20, 80))
    
    # Instructions
    for i, instruction in enumerate(instructions):
        instr_text = font.render(instruction, True, BLACK)
        screen.blit(instr_text, (20, 120 + i*25))
    
    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Play/Pause
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy() and not paused:
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    play_track()
            
            # Stop
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                paused = False
            
            # Next track
            elif event.key == pygame.K_n:
                current_track = (current_track + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                play_track()
            
            # Previous track
            elif event.key == pygame.K_p:
                current_track = (current_track - 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                play_track()
            
            # Volume up
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)
            
            # Volume down
            elif event.key == pygame.K_MINUS:
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)
            
            # Quit
            elif event.key == pygame.K_q:
                running = False
    
    draw_interface()
    pygame.time.Clock().tick(30)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()