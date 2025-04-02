import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Extended Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Snake block size
BLOCK_SIZE = 20

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (0, 0)
        self.length = 1
        self.score = 0
        self.level = 1

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = head_x + dir_x * BLOCK_SIZE
        new_y = head_y + dir_y * BLOCK_SIZE
        
        # Check for wall collision
        if new_x < 0 or new_x >= SCREEN_WIDTH or new_y < 0 or new_y >= SCREEN_HEIGHT:
            return True  # Game over
        
        # Check for self-collision
        if (new_x, new_y) in self.positions[1:]:
            return True  # Game over
        
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
        return False

    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

# Food class with different weights and timers
class Food:
    def __init__(self):
        self.weight = random.choice([1, 2, 3])  # 1, 2, or 3 points
        self.color = YELLOW if self.weight == 1 else RED if self.weight == 2 else BLUE
        self.spawn_time = time.time()
        self.lifetime = random.randint(3, 8)  # 3-8 seconds
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Game setup
snake = Snake()
food = Food()
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Main game loop
running = True
game_over = False
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))
            elif event.key == pygame.K_r and game_over:
                # Reset game
                snake = Snake()
                food = Food()
                game_over = False

    if not game_over:
        # Update snake
        game_over = snake.update()

        # Check if food is eaten
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += food.weight
            # Level up every 5 points
            if snake.score >= snake.level * 5:
                snake.level += 1
            food = Food()

        # Check if food expired
        if food.is_expired():
            food = Food()

        # Drawing
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)

        # Display score and level
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        level_text = font.render(f"Level: {snake.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
    else:
        # Game over screen
        game_over_text = font.render("Game Over! Press R to restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(10 + snake.level * 2)  # Speed increases with level

pygame.quit()
