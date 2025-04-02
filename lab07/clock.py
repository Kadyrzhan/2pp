import pygame
import time
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load Mickey image - INCREASED SIZE HERE (from 400x400 to 500x500)
try:
    mickey = pygame.image.load("mickey.png").convert_alpha()
    mickey = pygame.transform.scale(mickey, (500, 500))  # Bigger size
except:
    # Create a placeholder if image not found (also larger)
    mickey = pygame.Surface((600, 600), pygame.SRCALPHA)
    pygame.draw.circle(mickey, BLACK, (250, 250), 250)  # Bigger head
    pygame.draw.circle(mickey, WHITE, (180, 180), 50)  # Left ear
    pygame.draw.circle(mickey, WHITE, (320, 180), 40)  # Right ear

# Load or create clock hands (unchanged)
try:
    minute_hand_img = pygame.image.load("minute_hand.png").convert_alpha()
    second_hand_img = pygame.image.load("second_hand.png").convert_alpha()
except:
    minute_hand_img = pygame.Surface((10, 180), pygame.SRCALPHA)  # Slightly longer
    pygame.draw.line(minute_hand_img, BLACK, (5, 0), (5, 180), 10)  # Thicker
    
    second_hand_img = pygame.Surface((8, 220), pygame.SRCALPHA)  # Slightly longer
    pygame.draw.line(second_hand_img, RED, (4, 0), (4, 220), 6)  # Thicker

# Clock center (adjusted for larger Mickey)
clock_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def rotate_image(image, angle, pivot, offset_y):
    """Rotate an image around a pivot point with an offset."""
    rotated_image = pygame.transform.rotate(image, angle)
    offset = pygame.math.Vector2(0, -offset_y).rotate(-angle)
    rect_center = (pivot[0] + offset.x, pivot[1] + offset.y)
    rotated_rect = rotated_image.get_rect(center=rect_center)
    return rotated_image, rotated_rect

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    minute_angle = - (minutes * 6 + seconds * 0.1)
    second_angle = - (seconds * 6)

    screen.fill(WHITE)

    # Draw Mickey (centered with new size)
    screen.blit(mickey, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 250))  # Adjusted position

    # Draw hands (with slightly longer offsets to match bigger Mickey)
    minute_hand_rotated, minute_rect = rotate_image(minute_hand_img, minute_angle, clock_center, 70)
    second_hand_rotated, second_rect = rotate_image(second_hand_img, second_angle, clock_center, 70)
    
    screen.blit(minute_hand_rotated, minute_rect)
    screen.blit(second_hand_rotated, second_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()