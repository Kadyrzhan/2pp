import pygame
import pygame.gfxdraw
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Program")
clock = pygame.time.Clock()

# Default settings
drawing_color = BLACK
bg_color = WHITE
tool = "pen"  # pen, rectangle, circle, eraser
size = 5
start_pos = None

# Color palette
palette = [
    BLACK, WHITE, RED, GREEN, BLUE, 
    YELLOW, PURPLE, CYAN, 
    (255, 128, 0), (0, 128, 255), (255, 0, 128)
]

# Button class
class Button:
    def __init__(self, x, y, width, height, color, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 24)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        if self.text:
            text_surf = self.font.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
buttons = [
    Button(10, 10, 80, 40, WHITE, "Pen"),
    Button(100, 10, 80, 40, WHITE, "Rect"),
    Button(190, 10, 80, 40, WHITE, "Circle"),
    Button(280, 10, 80, 40, WHITE, "Eraser"),
    Button(SCREEN_WIDTH - 90, 10, 80, 40, WHITE, "Clear")
]

# Size selector
size_buttons = [
    Button(370, 10, 40, 40, WHITE, "S"),
    Button(420, 10, 40, 40, WHITE, "M"),
    Button(470, 10, 40, 40, WHITE, "L")
]

# Main game loop
running = True
screen.fill(bg_color)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Check tool buttons
            for i, button in enumerate(buttons):
                if button.is_clicked(pos):
                    if i == 0: tool = "pen"
                    elif i == 1: tool = "rectangle"
                    elif i == 2: tool = "circle"
                    elif i == 3: tool = "eraser"
                    elif i == 4: screen.fill(bg_color)
                    break
            
            # Check size buttons
            for i, button in enumerate(size_buttons):
                if button.is_clicked(pos):
                    if i == 0: size = 3
                    elif i == 1: size = 8
                    elif i == 2: size = 15
                    break
            
            # Check color palette
            for i, color in enumerate(palette):
                color_rect = pygame.Rect(10 + i*40, 60, 30, 30)
                if color_rect.collidepoint(pos):
                    drawing_color = color
                    break
            
            # Start drawing
            if pos[1] > 100:  # Below toolbar
                start_pos = pos
        
        if event.type == pygame.MOUSEBUTTONUP:
            if tool in ["rectangle", "circle"] and start_pos:
                end_pos = pygame.mouse.get_pos()
                if tool == "rectangle":
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(screen, drawing_color, rect, size)
                elif tool == "circle":
                    center = start_pos
                    radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(screen, drawing_color, center, radius, size)
            start_pos = None
        
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            
            # Don't draw on toolbar
            if pos[1] < 100:
                continue
            
            if tool == "pen":
                pygame.draw.circle(screen, drawing_color, pos, size)
            elif tool == "eraser":
                pygame.draw.circle(screen, bg_color, pos, size)
            elif tool in ["rectangle", "circle"]:
                pass  # Handled on mouse up
    
    # Draw toolbar background
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, SCREEN_WIDTH, 100))
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Draw size buttons
    for button in size_buttons:
        button.draw(screen)
    
    # Draw color palette
    for i, color in enumerate(palette):
        pygame.draw.rect(screen, color, (10 + i*40, 60, 30, 30))
        pygame.draw.rect(screen, BLACK, (10 + i*40, 60, 30, 30), 1)
    
    # Highlight selected tool
    if tool == "pen":
        pygame.draw.rect(screen, RED, buttons[0].rect, 3)
    elif tool == "rectangle":
        pygame.draw.rect(screen, RED, buttons[1].rect, 3)
    elif tool == "circle":
        pygame.draw.rect(screen, RED, buttons[2].rect, 3)
    elif tool == "eraser":
        pygame.draw.rect(screen, RED, buttons[3].rect, 3)
    
    # Highlight selected size
    if size == 3:
        pygame.draw.rect(screen, RED, size_buttons[0].rect, 3)
    elif size == 8:
        pygame.draw.rect(screen, RED, size_buttons[1].rect, 3)
    elif size == 15:
        pygame.draw.rect(screen, RED, size_buttons[2].rect, 3)
    
    # Display current color
    pygame.draw.rect(screen, drawing_color, (SCREEN_WIDTH - 140, 60, 50, 30))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 140, 60, 50, 30), 2)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()