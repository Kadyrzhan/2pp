import pygame
import time
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
CLOCK_CENTER = (WIDTH // 2, HEIGHT // 2)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)

# Load clock hand images
minute_hand = pygame.image.load("minute_hand.png")
second_hand = pygame.image.load("second_hand.png")

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock Application")
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Get time
    now = datetime.now()
    minutes_angle = -((now.minute % 60) * 6) + 90
    seconds_angle = -((now.second % 60) * 6) + 90
    
    # Rotate hands
    rotated_minute = pygame.transform.rotate(minute_hand, minutes_angle)
    rotated_second = pygame.transform.rotate(second_hand, seconds_angle)
    
    # Draw clock hands
    screen.blit(rotated_minute, rotated_minute.get_rect(center=CLOCK_CENTER))
    screen.blit(rotated_second, rotated_second.get_rect(center=CLOCK_CENTER))
    
    pygame.display.flip()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)

pygame.quit()