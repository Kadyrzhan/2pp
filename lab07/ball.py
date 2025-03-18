import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
BALL_RADIUS = 25
BALL_SPEED = 20
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Ball Movement")
clock = pygame.time.Clock()

# Ball position
ball_x, ball_y = WIDTH // 2, HEIGHT // 2

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)
    
    pygame.display.flip()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_y - BALL_RADIUS - BALL_SPEED >= 0:
                ball_y -= BALL_SPEED
            elif event.key == pygame.K_DOWN and ball_y + BALL_RADIUS + BALL_SPEED <= HEIGHT:
                ball_y += BALL_SPEED
            elif event.key == pygame.K_LEFT and ball_x - BALL_RADIUS - BALL_SPEED >= 0:
                ball_x -= BALL_SPEED
            elif event.key == pygame.K_RIGHT and ball_x + BALL_RADIUS + BALL_SPEED <= WIDTH:
                ball_x += BALL_SPEED
    
    clock.tick(30)

pygame.quit()
