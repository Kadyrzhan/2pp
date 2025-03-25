import pygame
import random
import time

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

# Game settings
PLAYER_SPEED = 5
ENEMY_SPEED = 3
COIN_SPAWN_RATE = 0.02  # 2% chance per frame

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

# Load images
def load_image(name, scale=1):
    img = pygame.image.load(name).convert_alpha()
    width = int(img.get_width() * scale)
    height = int(img.get_height() * scale)
    return pygame.transform.scale(img, (width, height))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("player.png", 0.1)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = PLAYER_SPEED
        self.coins = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
    
    def add_coin(self):
        self.coins += 1

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("enemy.png", 0.1)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
        self.speed = random.randint(ENEMY_SPEED, ENEMY_SPEED + 2)
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
            self.speed = random.randint(ENEMY_SPEED, ENEMY_SPEED + 2)

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("coin.png", 0.05)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -30)
        self.speed = random.randint(2, 4)
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Game setup
def game():
    # Create sprites groups
    player = Player()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    # Add initial enemies
    for i in range(5):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)
    
    # Font for displaying score
    font = pygame.font.SysFont(None, 36)
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Spawn coins randomly
        if random.random() < COIN_SPAWN_RATE:
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)
        
        # Update all sprites
        all_sprites.update()
        
        # Check for collisions with coins
        coin_hits = pygame.sprite.spritecollide(player, coins, True)
        for coin in coin_hits:
            player.add_coin()
        
        # Check for collisions with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            running = False
            game_over(player.coins)
        
        # Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Display coin count
        coin_text = font.render(f"Coins: {player.coins}", True, WHITE)
        screen.blit(coin_text, (SCREEN_WIDTH - 150, 20))
        
        pygame.display.flip()
        clock.tick(60)

# Game over screen
def game_over(coins):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    coin_text = small_font.render(f"You collected {coins} coins!", True, WHITE)
    restart_text = small_font.render("Press R to restart or Q to quit", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(coin_text, (SCREEN_WIDTH//2 - coin_text.get_width()//2, SCREEN_HEIGHT//2))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    return

# Main function
def main():
    game()
    pygame.quit()

if __name__ == "__main__":
    main()