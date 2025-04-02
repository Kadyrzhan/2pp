import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Extended Paint App")

# Create a separate canvas to persist drawings
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas.fill((255, 255, 255))  # White background

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Drawing variables
drawing = False
start_pos = None
current_color = BLACK
current_shape = "line"  # Default shape
shapes = ["line", "rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]
shape_index = 0

# Font for UI
font = pygame.font.SysFont(None, 24)

def draw_right_triangle(surface, color, start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [(x1, y1), (x2, y2), (x1, y2)]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, color, start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    side_length = max(abs(x2 - x1), abs(y2 - y1))
    height = side_length * math.sqrt(3) / 2
    points = [
        (x1, y1),
        (x1 + side_length, y1),
        (x1 + side_length // 2, y1 - height)
    ]
    pygame.draw.polygon(surface, color, points, 2)

def draw_rhombus(surface, color, start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]
    pygame.draw.polygon(surface, color, points, 2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Clear screen
                canvas.fill(WHITE)
            elif event.key == pygame.K_s:  # Change shape
                shape_index = (shape_index + 1) % len(shapes)
                current_shape = shapes[shape_index]
            elif event.key == pygame.K_1:
                current_color = RED
            elif event.key == pygame.K_2:
                current_color = GREEN
            elif event.key == pygame.K_3:
                current_color = BLUE
            elif event.key == pygame.K_4:
                current_color = BLACK
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            if start_pos:
                if current_shape == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, 2)
                elif current_shape == "rectangle":
                    pygame.draw.rect(canvas, current_color, 
                                    (start_pos[0], start_pos[1], 
                                     end_pos[0] - start_pos[0], 
                                     end_pos[1] - start_pos[1]), 2)
                elif current_shape == "circle":
                    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                elif current_shape == "square":
                    size = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], size, size), 2)
                elif current_shape == "right_triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos)
                elif current_shape == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos)
                elif current_shape == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos)

    # Render canvas
    screen.blit(canvas, (0, 0))

    # UI Display
    shape_text = font.render(f"Current Shape: {current_shape} (Press S to change)", True, BLACK)
    color_text = font.render("Colors: 1-Red, 2-Green, 3-Blue, 4-Black", True, BLACK)
    clear_text = font.render("Press C to clear screen", True, BLACK)
    screen.blit(shape_text, (10, 10))
    screen.blit(color_text, (10, 40))
    screen.blit(clear_text, (10, 70))

    pygame.display.flip()

pygame.quit()
