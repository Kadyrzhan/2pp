import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(name).convert_alpha()
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        return image
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        # Fallback surface if image not found
        surf = pygame.Surface((50, 80))
        surf.fill((255, 0, 0) if "enemy" in name else (0, 0, 255) if "player" in name else (255, 255, 0))
        return surf

# Load assets
player_img = load_image("player_car.png", 0.5)
enemy_img = load_image("enemy_car.png", 0.5)
coin_img = load_image("coin.png", 0.5)

# Player car
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Enemy car
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.y = -100
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
            self.rect.y = -100
            self.speed = random.randint(3, 6)

# Coin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.y = -30

    def update(self):
        self.rect.y += 4
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
            self.rect.y = -30

# Game setup
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = PlayerCar()
all_sprites.add(player)

for _ in range(5):
    enemy = EnemyCar()
    all_sprites.add(enemy)
    enemies.add(enemy)

for _ in range(3):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Coin collection
    hits = pygame.sprite.spritecollide(player, coins, True)
    for _ in hits:
        score += 1
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

    # Collision with enemies
    if pygame.sprite.spritecollide(player, enemies, False):
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
